import sys
import socket
from peer import Peer

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        name = socket.gethostname()
    except Exception:
        ip = '127.0.0.1'
        name = 'Guest'
    finally:
        sock.close()

    return ip, name

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'server'
    is_server = mode.lower() == 'server'

    host_ip, host_name = get_local_ip()
    print(f"[INFO] Detected local IP: {host_ip}")
    print(f"[INFO] Hostname: {host_name}")

    if is_server:
        # Server uses its own IP
        peer = Peer(is_server=True, host=host_ip)
    else:
        # Client connects to server IP passed as second arg
        peer = Peer(is_server=False, host=host_ip)

    peer.start()

if __name__ == "__main__":
    main()

