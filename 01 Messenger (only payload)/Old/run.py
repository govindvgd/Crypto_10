import sys              # Used to access command-line arguments
from peer import Peer   # Imports the Peer class that manages secure communication

def main():
    # Check if a mode (e.g., 'client' or 'server') was passed as a command-line argument
    # Defaults to 'server' if no argument is provided
    mode = sys.argv[1] if len(sys.argv) > 1 else 'server'
    
    # Determine whether this instance should act as a server
    is_server = mode.lower() == 'server'

    # Create a Peer instance with the role (server/client)
    peer = Peer(is_server)

    # Start the peer: initialize socket, perform handshake, and launch send/receive loops
    peer.start()

# Ensures that main() is only called when this script is executed directly,
# not when it's imported as a module in another script.
if __name__ == "__main__":
    main()

