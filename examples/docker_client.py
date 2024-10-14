from time import sleep

from simple_node import SimpleNodeClient

if __name__ == "__main__":
    client = SimpleNodeClient("localhost:35701", "localhost:35700")
    client.join_network()
    sleep(1)

    print("Sending a print message")
    client.send("print", ["Data to be printed"], client.server_id)

