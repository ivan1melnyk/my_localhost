from thread_maker import ServerThread,  ClientThread

if __name__ == '__main__':
    server = ServerThread()
    client = ClientThread()
    server.start()
    client.start()
