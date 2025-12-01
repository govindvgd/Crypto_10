from crypto_utils import load_public_key  # Make sure this function exists
from crypto_utils import *
import socket
import threading
import struct
from crypto_utils import load_public_key, rsa_encrypt, generate_symmetric_key, aesgcm_encrypt, aesgcm_decrypt

def read_n(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed while reading")
        buf += chunk
    return buf

class Peer:
    def __init__(self, is_server=False, host='127.0.0.1', port=5002):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.symmetric_key = None

    def start(self):
        if self.is_server:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            self.conn = conn
            self._do_handshake_server()
        else:
            self.sock.connect((self.host, self.port))
            self.conn = self.sock
            self._do_handshake_client()

        self._start_threads()

    def _do_handshake_client(self):
        # receive server public key
        length_bytes = read_n(self.conn, 4)
        l = struct.unpack('!I', length_bytes)[0]
        pub_bytes = read_n(self.conn, l)
        pub = load_public_key(pub_bytes)
        # generate symmetric key and send it encrypted with server pubkey
        sym = generate_symmetric_key()
        enc_sym = rsa_encrypt(pub, sym)
        self.conn.sendall(struct.pack('!I', len(enc_sym)) + enc_sym)
        self.symmetric_key = sym
        print("[*] Handshake complete: symmetric key established")

    def _do_handshake_server(self):
        raise RuntimeError("This Peer instance is configured as client; _do_handshake_server not used.")

    def _start_threads(self):
        threading.Thread(target=self._receive_loop, daemon=True).start()
        print("Ready (encrypted channel)")
        self._send_loop()

    def _receive_loop(self):
        while True:
            try:
                length_bytes = self.conn.recv(4)
                if not length_bytes:
                    print("\n[Peer disconnected]")
                    break
                l = struct.unpack('!I', length_bytes)[0]
                data = read_n(self.conn, l)
                try:
                    plain = aesgcm_decrypt(self.symmetric_key, data)
                    message = plain.decode()
                except Exception:
                    print("[!] Failed to decrypt message")
                    continue
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
                enc = aesgcm_encrypt(self.symmetric_key, msg.encode())
                self.conn.sendall(struct.pack('!I', len(enc)) + enc)
                if msg.lower() == "exit":
                    break
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





