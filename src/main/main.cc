#include "CacheNode.h"
#include <iostream>
#include <string>

using namespace cache_node;

int main(int argc, char* argv[]) {
  string node_id = "node1";
  string node_server = "node2";
  CacheNodeClient node = CacheNodeClient(node_id, node_server);
  return 0;
}
