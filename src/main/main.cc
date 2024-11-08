// #include "AtomSpaceNode.h"
#include "mqtt/client.h"
#include <iostream>
#include <string>

using namespace mqtt_client;

int main(int argc, char *argv[]) {
  // Define the server address, client ID, topics to subscribe to, and QoS
  int qos = 1;
  std::vector<std::string> topics = {"test/broadcast", "test/self"};

  // Define a custom callback function
  auto custom_callback = [](const MqttMessage &msg) {
    std::cout << "Custom Callback: Message received on topic '" << msg.topic
              << "' with payload: " << msg.payload << std::endl;
  };

  // Create the client and start it, passing the custom callback
  MqttClient client("tcp://donaldduck.local:1883", "client_id_123", topics, qos,
                    custom_callback);
  client.start();

  // Send a message to a topic
  client.send_message(MqttMessage("test/broadcast", "Hello, MQTT"));

  // Run the client (it will keep running until stopped)
  std::this_thread::sleep_for(std::chrono::seconds(10));

  client.stop();
  return 0;
}
