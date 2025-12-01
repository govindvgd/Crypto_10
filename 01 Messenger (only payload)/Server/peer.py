import socket
import threading

class Peer:
    def __init__(self, is_server=True, host='0.0.0.0', port=5002):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_server = is_server
        self.host = host
        self.port = port
        self.conn = None

    def start(self):
        if self.is_server:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print(f"[*] Listening on {self.host}:{self.port} ...")
            conn, addr = self.sock.accept()
            print(f"[*] Connection from {addr}")
            self.conn = conn
        else:
            self.sock.connect((self.host, self.port))
            self.conn = self.sock

        self._start_threads()

    def _start_threads(self):
        threading.Thread(target=self._receive_loop, daemon=True).start()
        print("I'm ready")
        self._send_loop()

    def _receive_loop(self):
        while True:
            try:
                data = self.conn.recv(4096)
                if not data:
                    print("\n[Peer disconnected]")
                    break
                message = data.decode()
                if message.strip().lower() == "exit":
                    print("\n[Peer exited]")
                    break
                print(f"\n[Peer]: {message}")
            except Exception as e:
                print(f"[Receive error]: {e}")
                break

    def _send_loop(self):
        while True:
            try:
                msg = input("You: ").strip()
                if not msg:
                    continue
                if msg.lower() == "exit":
                    self.conn.sendall(msg.encode())
                    break
                self.conn.sendall(msg.encode())
            except Exception as e:
                print(f"[Send error]: {e}")
                break

        try:
            self.conn.close()
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        print("[*] Connection closed.")





