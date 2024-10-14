from simple_node import SimpleNodeServer

if __name__ == "__main__":
    server = SimpleNodeServer("localhost:35700")
    server.join_network()
