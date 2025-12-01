import sys
from peer import Peer

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5002
    host = '0.0.0.0'
    peer = Peer(is_server=True, host=host, port=port)
    peer.start()

if __name__ == "__main__":
    main()

