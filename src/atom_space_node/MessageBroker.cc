#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>
#include <grpcpp/channel.h>
#include <grpcpp/client_context.h>
#include <grpcpp/create_channel.h>
#include <grpcpp/security/credentials.h>


#include "common.pb.h"
#include "atom_space_node.grpc.pb.h"
#include "atom_space_node.pb.h"

#include "Utils.h"
#include "MessageBroker.h"

using namespace atom_space_node;

unsigned int SynchronousGRPC::MESSAGE_THREAD_COUNT = 10;
unsigned int SynchronousSharedRAM::MESSAGE_THREAD_COUNT = 1;
unordered_map<string, RequestQueue *> SynchronousSharedRAM::NODE_QUEUE;
mutex SynchronousSharedRAM::NODE_QUEUE_MUTEX;

// -------------------------------------------------------------------------------------------------
// Constructors and destructors

MessageBroker *MessageBroker::factory(
    MessageBrokerType instance_type,
    MessageFactory *host_node,
    const string &node_id) {

    switch (instance_type) {
        case MessageBrokerType::RAM : {
            return new SynchronousSharedRAM(host_node, node_id);
        }
        case MessageBrokerType::GRPC : {
            return new SynchronousGRPC(host_node, node_id);
        }
        default: {
            Utils::error("Invalid MessageBrokerType: " + to_string((int) instance_type));
            return NULL; // to avoid warnings
        }
    }
}

MessageBroker::MessageBroker(MessageFactory *host_node, const string &node_id) {
    this->host_node = host_node;
    this->node_id = node_id;
    this->shutdown_flag = false;
}

MessageBroker::~MessageBroker() {
}

SynchronousSharedRAM::SynchronousSharedRAM(
    MessageFactory *host_node,
    const string &node_id) : MessageBroker(host_node, node_id) {
}

SynchronousSharedRAM::~SynchronousSharedRAM() {
    graceful_shutdown();
    for (auto thread: inbox_threads) {
        thread->join();
    }
    NODE_QUEUE_MUTEX.lock();
    if (NODE_QUEUE.find(this->node_id) == NODE_QUEUE.end()) {
        NODE_QUEUE_MUTEX.unlock();
        Utils::error("Unable to remove node from network: " + this->node_id);
    } else {
        NODE_QUEUE.erase(this->node_id);
        NODE_QUEUE_MUTEX.unlock();
    }
}

SynchronousGRPC::SynchronousGRPC(
    MessageFactory *host_node,
    const string &node_id) : MessageBroker(host_node, node_id) {
}

SynchronousGRPC::~SynchronousGRPC() {
    graceful_shutdown();
    for (auto thread: inbox_threads) {
        thread->join();
    }
    for (auto thread: outbox_threads) {
        thread->join();
    }
    grpc_server->Shutdown();
}

// -------------------------------------------------------------------------------------------------
// Methods used to start threads

void SynchronousGRPC::grpc_thread_method() {
    std::string server_address = this->node_id;
    grpc::EnableDefaultHealthCheckService(true);
    grpc::reflection::InitProtoReflectionServerBuilderPlugin();
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(this);
    std::cout << "SynchronousGRPC listening on " << server_address << std::endl;
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    grpc_server = std::move(server);
    grpc_server->Wait();
}

void SynchronousSharedRAM::inbox_thread_method() {
    bool stop_flag = false;
    do {
        void *request = this->incoming_messages.dequeue();
        if (request != NULL) {
            CommandLinePackage *message_data = (CommandLinePackage *) request;
            if (message_data->is_broadcast) {
                if (message_data->visited.find(this->node_id) != message_data->visited.end()) {
                    continue;
                }
                this->peers_mutex.lock();
                for (auto target: this->peers) {
                    if (message_data->visited.find(target) == message_data->visited.end()) {
                        CommandLinePackage *command_line = new CommandLinePackage(
                            message_data->command,
                            message_data->args);
                        command_line->is_broadcast = true;
                        command_line->visited = message_data->visited;
                        command_line->visited.insert(this->node_id);
                        NODE_QUEUE[target]->enqueue((void *) command_line);
                    }
                }
                this->peers_mutex.unlock();
            }
            std::unique_ptr<Message> message = this->host_node->message_factory(message_data->command, message_data->args);
            if (! message) {
                Utils::error("Invalid NULL Message");
            }
            if (this->host_node == NULL) {
                Utils::error("Invalid NULL host_node");
            }
            message->act((AtomSpaceNode *) this->host_node);
            delete message_data;
        } else {
            if (this->is_shutting_down()) {
                stop_flag = true;
            } else {
                Utils::sleep();
            }
        }
    } while (! stop_flag);
}

void SynchronousGRPC::inbox_thread_method() {
    bool stop_flag = false;
    do {
        void *request = this->incoming_messages.dequeue();
        if (request != NULL) {
            dasproto::MessageData *message_data = (dasproto::MessageData *) request;
            if (message_data->is_broadcast()) {
                this->peers_mutex.lock();
                unsigned int num_peers = this->peers.size();
                this->peers_mutex.unlock();
                if (num_peers > 0) {
                    dasproto::Empty reply[num_peers];
                    grpc::ClientContext context[num_peers];
                    unsigned int cursor = 0;
                    unordered_set<string> visited;
                    int num_visited = message_data->visited_recipients_size();
                    for (int i = 0; i < num_visited; i++) {
                        visited.insert(message_data->visited_recipients(i));
                    }
                    if (visited.find(this->node_id) != visited.end()) {
                        continue;
                    }
                    message_data->add_visited_recipients(this->node_id);
                    this->peers_mutex.lock();
                    for (auto target: this->peers) {
                        if (visited.find(target) == visited.end()) {
                            auto stub = dasproto::AtomSpaceNode::NewStub(grpc::CreateChannel(target, grpc::InsecureChannelCredentials()));
                            stub->execute_message(&(context[cursor]), *message_data, &(reply[cursor]));
                            cursor++;
                        }
                    }
                    this->peers_mutex.unlock();
                }
            }
            string command = message_data->command();
            vector<string> args;
            int num_args = message_data->args_size();
            for (int i = 0; i < num_args; i++) {
                args.push_back(message_data->args(i));
            }
            std::unique_ptr<Message> message = this->host_node->message_factory(command, args);
            if (! message) {
                Utils::error("Invalid NULL Message");
            }
            if (this->host_node == NULL) {
                Utils::error("Invalid NULL host_node");
            }
            message->act((AtomSpaceNode *) this->host_node);
        } else {
            if (this->is_shutting_down()) {
                stop_flag = true;
            } else {
                Utils::sleep();
            }
        }
    } while (! stop_flag);
}

void SynchronousGRPC::outbox_thread_method() {
    bool stop_flag = false;
    // TODO Implement this method
    do {
        if (this->is_shutting_down()) {
            stop_flag = true;
        } else {
            Utils::sleep();
        }
    } while (! stop_flag);
}

// -------------------------------------------------------------------------------------------------
// MessageBroker API

void MessageBroker::add_peer(const string &peer_id) {
    peers_mutex.lock();
    peers.insert(peer_id);
    peers_mutex.unlock();
}

bool MessageBroker::is_peer(const string &peer_id) {
    bool answer = true;
    this->peers_mutex.lock();
    if (peers.find(peer_id) == peers.end()) {
        answer = false;
    }
    this->peers_mutex.unlock();
    return answer;
}

void MessageBroker::graceful_shutdown() {
    this->shutdown_flag_mutex.lock();
    this->shutdown_flag = true;
    this->shutdown_flag_mutex.unlock();
}

bool MessageBroker::is_shutting_down() {
    bool answer;
    this->shutdown_flag_mutex.lock();
    answer = this->shutdown_flag;
    this->shutdown_flag_mutex.unlock();
    return answer;
}

// ----------------------------------------------------------------
// SynchronousSharedRAM

void SynchronousSharedRAM::join_network() {
    NODE_QUEUE_MUTEX.lock();
    if (NODE_QUEUE.find(this->node_id) != NODE_QUEUE.end()) {
        NODE_QUEUE_MUTEX.unlock();
        Utils::error("Node ID already in the network: " + this->node_id);
    } else {
        NODE_QUEUE[this->node_id] = &(this->incoming_messages);
        NODE_QUEUE_MUTEX.unlock();
    }
    for (unsigned int i = 0; i < MESSAGE_THREAD_COUNT; i++) {
        this->inbox_threads.push_back(new thread(
            &SynchronousSharedRAM::inbox_thread_method,
            this));
    }
}

void SynchronousSharedRAM::send(
    const string &command,
    const vector<string> &args,
    const string &recipient) {

    if (! this->is_shutting_down()) {
        if (! is_peer(recipient)) {
            Utils::error("Unknown peer: " + recipient);
        }
        CommandLinePackage *command_line = new CommandLinePackage(command, args);
        NODE_QUEUE[recipient]->enqueue((void *) command_line);
    }
}

void SynchronousSharedRAM::broadcast(const string &command, const vector<string> &args) {
    if (! this->is_shutting_down()) {
        this->peers_mutex.lock();
        unsigned int num_peers = this->peers.size();
        if (num_peers == 0) {
            this->peers_mutex.unlock();
            return;
        }
        CommandLinePackage *command_line;
        for (auto peer_id: this->peers) {
            command_line = new CommandLinePackage(command, args);
            command_line->is_broadcast = true;
            command_line->visited.insert(this->node_id);
            NODE_QUEUE[peer_id]->enqueue((void *) command_line);
        }
        this->peers_mutex.unlock();
    }
}

// ----------------------------------------------------------------
// SynchronousGRPC

void SynchronousGRPC::join_network() {
    this->grpc_thread = new std::thread(&SynchronousGRPC::grpc_thread_method, this);
    for (unsigned int i = 0; i < MESSAGE_THREAD_COUNT; i++) {
        this->inbox_threads.push_back(new thread(
            &SynchronousGRPC::inbox_thread_method,
            this));
        this->outbox_threads.push_back(new thread(
            &SynchronousGRPC::outbox_thread_method,
            this));
    }
}

void SynchronousGRPC::add_peer(const string &peer_id) {
    MessageBroker::add_peer(peer_id);
}

void SynchronousGRPC::send(
    const string &command,
    const vector<string> &args,
    const string &recipient) {

    if (! is_peer(recipient)) {
        Utils::error("Unknown peer: " + recipient);
    }
    dasproto::MessageData message_data;
    message_data.set_command(command);
    for (auto arg: args) {
        message_data.add_args(arg);
    }
    message_data.set_sender(this->node_id);
    message_data.set_is_broadcast(false);
    dasproto::Empty reply;
    grpc::ClientContext context;
    auto stub = dasproto::AtomSpaceNode::NewStub(grpc::CreateChannel(recipient, grpc::InsecureChannelCredentials()));
    stub->execute_message(&context, message_data, &reply);
}

void SynchronousGRPC::broadcast(const string &command, const vector<string> &args) {
    this->peers_mutex.lock();
    unsigned int num_peers = this->peers.size();
    if (num_peers == 0) {
        this->peers_mutex.unlock();
        return;
    }
    dasproto::Empty reply[num_peers];
    grpc::ClientContext context[num_peers];
    unsigned int cursor = 0;
    for (auto peer_id: this->peers) {
        dasproto::MessageData message_data;
        message_data.set_command(command);
        for (auto arg: args) {
            message_data.add_args(arg);
        }
        message_data.set_sender(this->node_id);
        message_data.set_is_broadcast(true);
        message_data.add_visited_recipients(this->node_id);
        auto stub = dasproto::AtomSpaceNode::NewStub(grpc::CreateChannel(peer_id, grpc::InsecureChannelCredentials()));
        stub->execute_message(&(context[cursor]), message_data, &(reply[cursor]));
        cursor++;
    }
    this->peers_mutex.unlock();
}

// -------------------------------------------------------------------------------------------------
// GRPC Server API

grpc::Status SynchronousGRPC::ping(
    grpc::ServerContext* grpc_context,
    const dasproto::Empty* request,
    dasproto::Ack* reply) {

    reply->set_msg("PING");
    if (! this->is_shutting_down()) {
        return grpc::Status::OK;
    } else {
        return grpc::Status::CANCELLED;
    }
}

grpc::Status SynchronousGRPC::execute_message(
    grpc::ServerContext* grpc_context,
    const dasproto::MessageData* request,
    dasproto::Empty* reply) {

    if (! this->is_shutting_down()) {
        // TODO: fix memory leak
        this->incoming_messages.enqueue((void *) new dasproto::MessageData(*request));
        return grpc::Status::OK;
    } else {
        return grpc::Status::CANCELLED;
    }
}

// -------------------------------------------------------------------------------------------------
// Common utility classes

CommandLinePackage::CommandLinePackage(const string &command, const vector<string> &args) {
    this->command = command;
    this->args = args;
    this->is_broadcast = false;
}

CommandLinePackage::~CommandLinePackage() {
}
