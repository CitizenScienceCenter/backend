from app import Server

server = Server()
application = server.connexion_app.app

if __name__ == "__main__":
    server.run()
