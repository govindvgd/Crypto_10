import sys
from peer import Peer

def main():
    # Accept optional port argument. Always run as server.
    port = 5002
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 alt_run_server.py [port]")
            return

    host = '0.0.0.0'  # listen on all interfaces
    peer = Peer(is_server=True, host=host, port=port)
    peer.start()

if __name__ == "__main__":
    main()

