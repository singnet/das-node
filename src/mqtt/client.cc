#include "client.h"

MQTTClient::MQTTClient(
    const std::string &server_address, const std::string &client_id,
    const std::vector<std::string> &topics, const int qos,
    std::function<void(const MqttMessage &)> message_callback)
    : client_(server_address, client_id), topics_(topics), qos_(qos),
      is_running_(false), message_callback_(message_callback) {
  client_.set_callback(*this);
}

MQTTClient::~MQTTClient() { stop(); }

void MQTTClient::start() {
  mqtt::connect_options connOpts;
  connOpts.set_clean_session(true);

  try {
    std::cout << "Connecting to the MQTT broker at " << client_.get_server_uri()
              << "..." << std::endl;
    client_.connect(connOpts)->wait();
    std::cout << "Connected!" << std::endl;

    is_running_ = true;

    // Start separate threads for publishing and subscribing
    pub_thread_ = std::thread(&MQTTClient::publish_loop, this);
    sub_thread_ = std::thread(&MQTTClient::subscribe_loop, this);
  } catch (const mqtt::exception &exc) {
    std::cerr << "Error: " << exc.what() << std::endl;
  }
}

void MQTTClient::stop() {
  if (is_running_) {
    is_running_ = false;

    if (pub_thread_.joinable())
      pub_thread_.join();
    if (sub_thread_.joinable())
      sub_thread_.join();

    try {
      client_.disconnect()->wait();
      std::cout << "Disconnected!" << std::endl;
    } catch (const mqtt::exception &exc) {
      std::cerr << "Error: " << exc.what() << std::endl;
    }
  }
}

void MQTTClient::send_message(const MqttMessage msg) {
  std::lock_guard<std::mutex> lock(queue_mutex_);
  message_queue_.push_back(msg);
}

void MQTTClient::message_arrived(mqtt::const_message_ptr msg) {
  // Call the user-defined callback function with the received message
  MqttMessage mqtt_msg(msg->get_topic(), msg->get_payload_str());
  message_callback_(mqtt_msg);
}

void MQTTClient::connection_lost(const std::string &cause) {
  std::cerr << "Connection lost: " << cause << std::endl;
  is_running_ = false;
}

void MQTTClient::publish_loop() {
  while (is_running_) {
    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::lock_guard<std::mutex> lock(queue_mutex_);
    for (const auto &msg : message_queue_) {
      auto pubmsg = mqtt::make_message(msg.topic, msg.payload);
      pubmsg->set_qos(qos_);

      try {
        client_.publish(pubmsg)->wait();
        std::cout << "Published message: " << msg.payload << " to " << msg.topic
                  << std::endl;
      } catch (const mqtt::exception &exc) {
        std::cerr << "Publish error: " << exc.what() << std::endl;
      }
    }
    message_queue_.clear(); // Clear messages after publishing
  }
}

void MQTTClient::subscribe_loop() {
  try {
    for (const auto &topic : topics_) {
      client_.subscribe(topic, qos_)->wait();
      std::cout << "Subscribed to topic: " << topic << std::endl;
    }

    while (is_running_) {
      std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
  } catch (const mqtt::exception &exc) {
    std::cerr << "Subscribe error: " << exc.what() << std::endl;
  }
}

int main() {
  // Define the server address, client ID, topics to subscribe to, and QoS
  int qos = 1;
  std::vector<std::string> topics = {"test/broadcast", "test/self"};

  // Define a custom callback function
  auto custom_callback = [](const MqttMessage &msg) {
    std::cout << "Custom Callback: Message received on topic '" << msg.topic
              << "' with payload: " << msg.payload << std::endl;
  };

  // Create the client and start it, passing the custom callback
  MQTTClient client("tcp://donaldduck.local:1883", "client_id_123", topics, qos,
                    custom_callback);
  client.start();

  // Send a message to a topic
  client.send_message(MqttMessage("test/broadcast", "Hello, MQTT"));

  // Run the client (it will keep running until stopped)
  std::this_thread::sleep_for(std::chrono::seconds(10));

  client.stop();
  return 0;
}
