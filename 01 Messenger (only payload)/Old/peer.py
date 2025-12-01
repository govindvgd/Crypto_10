import socket
import threading

class Peer:
    def __init__(self, is_server, host='127.0.0.1', port=5000): # port=0 means OS picks
        # Initialize a TCP socket
        self.sock = socket.socket()
        
        # True if this peer should act as a server
        self.is_server = is_server
        
        # IP address and port to bind or connect to
        self.host = host
        self.port = port
        print(self.host)


    def start(self):
        """Starts the peer in either server or client mode, performs handshake, and launches communication threads."""
        if self.is_server:
            # Server binds and listens for one connection
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print("[*] Waiting for connection...")
            conn, _ = self.sock.accept()
            client_ip, client_port = conn.getpeername()
            print(f"Client connected from IP: {client_ip}, Port: {client_port}")
            self.conn = conn  # Store the accepted connection
            #print(self.conn)
        else:
            # Client connects to the server
            self.sock.connect((self.host, self.port))
            self.conn = self.sock  # Use socket itself for client
            #print(self.conn)

        # Start send and receive loops
        self._start_threads()


    def _start_threads(self):
        """Starts a background thread for receiving and enters sending loop in the main thread."""
        # Start receiving in a daemon thread
        threading.Thread(target=self._receive_loop, daemon=True).start()
        print("I'm ready")
        
        # Start sending in the main thread
        self._send_loop()


    def _receive_loop(self):
        """Receives and prints plain text messages from the peer."""
        while True:
            data = self.conn.recv(4096)
            if not data:
                #print("going to break")
                break  # Connection closed
            print(f"\n[Peer]: {data.decode()}")
            

    def _send_loop(self):
        """Reads user input and sends it as plain text to the peer."""
        while True:
            msg = input("You: ").strip().encode()
            self.conn.sendall(msg)
            

