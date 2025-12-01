# Python Secure Messaging Demos

This repository demonstrates socket-based communication in Python, progressing from simple plaintext messaging to a secure, encrypted chat application using the `cryptography` library.

## Projects Overview

1.  **01 Messenger (only payload)**
    *   A basic TCP client-server chat application.
    *   Transmits messages in plain text (unencrypted).
    *   Demonstrates basic socket handling and threading.

2.  **02 Messenger (Handshaking)**
    *   A secure hybrid encryption chat application.
    *   **Handshake:** Uses **RSA** (Asymmetric) to securely exchange a session key.
    *   **Transport:** Uses **AES-GCM** (Symmetric) for authenticated encryption of the chat messages.
    *   Demonstrates key generation, serialization, and stream framing.

---

## Prerequisites

*   Python 3.6+
*   `cryptography` library

### Installation

It is recommended to use a virtual environment.

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install cryptography
```

---

## Usage

Open two terminal windows (one for Server, one for Client) and run the commands below from the repository root.

### Demo 1: Plaintext Messenger

**Server:**
```bash
cd "01 Messenger (only payload)/Server"
python3 alt_run_server.py
```

**Client:**
```bash
cd "01 Messenger (only payload)/Client"
# Usage: python3 alt_run_client.py <server_ip>
python3 alt_run_client.py 127.0.0.1
```

### Demo 2: Encrypted Messenger (Handshaking)

**Server:**
```bash
cd "02 Messenger (Handshaking)/Server"
python3 alt_run_server.py
```

**Client:**
```bash
cd "02 Messenger (Handshaking)/Client"
# Usage: python3 alt_run_client.py <server_ip>
python3 alt_run_client.py 127.0.0.1
```

*Type messages in the prompt. Type `exit` to close the connection.*

---

## Technical Implementation Details

### The Cryptographic Handshake (Demo 02)
1.  **Server Startup:** Generates an ephemeral RSA keypair.
2.  **Connection:** Server sends its **Public Key** (PEM format) to the Client.
3.  **Key Exchange:** Client generates a random 32-byte **AES Session Key**, encrypts it using the Server's Public Key (OAEP padding), and sends it back.
4.  **Secure Session:** Both parties now possess the same AES key.

### Message Transport
*   **Encryption:** AES-256-GCM (Galois/Counter Mode) provides both confidentiality and integrity.
*   **Framing:** TCP is a stream protocol. To ensure complete message delivery, we use a 4-byte length prefix (Big Endian) before sending the encrypted payload.
*   **Nonces:** A unique 12-byte nonce is generated for every message and prepended to the ciphertext.
