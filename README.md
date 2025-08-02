# 🔐 Token-Based Network Authentication Server

This project provides a foundational server-side system for authenticating clients over both **TCP** and **UDP** protocols using **UUID+TOKEN** validation. Although the client side is currently incomplete, the server handles basic requests, verifies tokens, and stores client data securely using SQLite.

## ⚙️ Features

- Dual protocol support: **TCP + UDP**
- Auto-generation and validation of **UUID-TOKEN** pairs
- Lightweight **JSON configuration** file with debug settings
- ANSI-colored console logging for enhanced readability
- SQLite-based persistent storage for user and token records
- Secure access control via a static key file (`TheKey.key`)

## 🧪 Current Scope

This implementation is server-only. Clients are expected to:
1. Receive a generated token upon UDP interaction
2. Send the token via TCP for authentication
3. Receive response: either `ONAYLANDI` (accepted) or `REDDEDILDI` (denied)

The system is functional but basic. Client-side logic (token handling, UI, handshake feedback, etc.) remains a future enhancement.

## 📁 File Structure Overview

| File                | Description                                  |
|---------------------|----------------------------------------------|
| `main.py`           | Core server logic                            |
| `config.json`       | Configuration file (IP/ports/debug levels)   |
| `TheKey.key`        | Static access key for system initialization  |
| `Database.db`       | SQLite database storing UUIDs and tokens     |

## 🧵 Main Components

- `GetKey()` — Verifies access key
- `GetJSONConfig()` — Loads or creates JSON config
- `ConnectDB()` — Establishes SQLite connection, creates tables
- `ServerTCP()` — TCP socket operations & token validation
- `ServerUDP()` — UDP socket listener & client token generation

## 🚀 Getting Started

```bash
python main.py
