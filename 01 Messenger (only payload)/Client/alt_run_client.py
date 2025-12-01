import sys
import socket
from peer import Peer

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 alt_run_client.py <server_ip> [port]")
        return
    server_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5002
    host_ip = get_local_ip()
    print(f"[INFO] Local IP: {host_ip}")
    peer = Peer(is_server=False, host=server_ip, port=port)
    peer.start()

if __name__ == "__main__":
    main()

