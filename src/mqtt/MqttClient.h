#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <atomic>
#include <functional>
#include <iostream>
#include <mqtt/async_client.h>
#include <mutex>
#include <thread>
#include <vector>

using namespace mqtt;
using namespace std;

namespace mqtt_client {

// MQTTMessage structure to hold message payload and topic
struct MqttMessage {
  std::string topic;
  std::string payload;

  MqttMessage(const std::string &t, const std::string &p)
      : topic(t), payload(p) {};
};

// MQTTClient class for handling both publishing and subscribing
class MqttClient : public virtual mqtt::callback {
public:
  // Constructor to initialize client with server address, client ID, topics,
  // QoS, and callback
  MqttClient(const std::string &server_address, const std::string &client_id,
             const std::vector<std::string> &topics, const int qos,
             std::function<void(const MqttMessage &)> message_callback);

  // Destructor to clean up resources
  ~MqttClient();

  // Start the client and its threads for publishing and subscribing
  void start();

  // Stop the client and its threads
  void stop();

  // Send a message to a specific topic
  void send_message(const MqttMessage msg);

private:
  // MQTT client object
  mqtt::async_client client_;

  // List of topics to subscribe to
  std::vector<std::string> topics_;

  // QoS level
  const int qos_;

  // Flag to indicate if the client is running
  std::atomic<bool> is_running_;

  // Threads for publishing and subscribing
  std::thread pub_thread_;
  std::thread sub_thread_;

  // Message queue for outgoing messages
  std::vector<MqttMessage> message_queue_;
  std::mutex queue_mutex_; // Mutex to protect the message queue

  // User-defined callback function to handle received messages
  std::function<void(const MqttMessage &)> message_callback_;

  // Callback method for when a message is received
  void message_arrived(mqtt::const_message_ptr msg) override;

  // Callback for when the connection is lost
  void connection_lost(const std::string &cause) override;

  // Method to publish messages from the queue
  void publish_loop();

  // Method to subscribe and listen for incoming messages
  void subscribe_loop();
};

} // namespace mqtt_client
#endif // MQTT_CLIENT_H
