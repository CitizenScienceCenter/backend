from app import Server

server = Server()
application = server.app.app

if __name__ == "__main__":
    server.run()
