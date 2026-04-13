# HTTPS Webpage Downloader & Analyzer

> A computer networks educational project that exposes the internal mechanics of secure web communication — step by step, in real time.

---

## What It Does

Most people use HTTPS every day without knowing what happens under the hood. This project pulls back the curtain. Enter any URL and watch the full connection lifecycle execute live — from DNS lookup to TLS handshake to HTML response — with every step logged and explained.

Built with **Python (Flask + raw sockets + ssl)** on the backend and a **pure HTML/CSS/JS** frontend. No high-level libraries. No curl. No magic.

---

## Features

- Real DNS resolution using the OS resolver
- Actual TCP 3-way handshake (SYN → SYN-ACK → ACK) with measured RTT
- Live TLS handshake — shows version, cipher suite, and certificate validity
- Full HTTP/1.1 GET request and response parsing
- Animated pipeline visualizer in the browser
- Clearly separated output sections for each step
- Download the full session log as a `.txt` file
- Built-in Help and Developed By sections

---

## Project Structure

```
http-analyzer/
├── app.py              # Flask server — routes and API
├── DA_1.py             # Core downloader — sockets, SSL, HTTP
├── static/
│   ├── dev1.jpg        # Developer 1 photo
│   └── dev2.jpg        # Developer 2 photo
└── templates/
    └── index.html      # Frontend — UI, simulation, visualization
```

---

## How It Works

Each time you submit a URL, the backend runs through 6 real networking steps:

| Step | What Happens |
|------|-------------|
| 1 | **URL Parsing** — scheme, host, port, and path are extracted |
| 2 | **DNS Resolution** — hostname is resolved to an IP address |
| 3 | **TCP Handshake** — a socket connects and the 3-way handshake completes |
| 4 | **TLS Handshake** — encrypted channel is negotiated (cipher, cert verified) |
| 5 | **HTTP GET Request** — request is sent manually over the encrypted connection |
| 6 | **Response** — server reply is received, headers parsed, status logged |

Every step is returned to the frontend as structured JSON and rendered live in the terminal output, with the pipeline diagram animating as each phase completes.

---

## Getting Started

### Requirements

- Python 3.8 or higher
- Flask

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/http-analyzer.git
cd http-analyzer

# Install Flask
pip install flask

# Run the app
python app.py
```

Then open your browser and go to:

```
http://localhost:5000
```

### Usage

1. Enter any domain in the input box — e.g. `example.com` or `https://google.com`
2. Click **RUN**
3. Watch each step execute live in the terminal output
4. Click **DOWNLOAD OUTPUT** to save the session log as a `.txt` file

> **Tip:** Some sites block programmatic access. `example.com` is a reliable test target.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Networking | `socket`, `ssl`, `urllib.parse` |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Fonts | Orbitron, Share Tech Mono (Google Fonts) |

---

## Concepts Demonstrated

This project is a practical implementation of core Computer Networks topics:

- **Application Layer** — HTTP/1.1 request-response model
- **Transport Layer** — TCP connection setup and teardown
- **Network Layer** — DNS resolution and IP addressing
- **Security** — TLS 1.2/1.3 handshake, certificate verification, cipher negotiation

---

## Academic Context

- **Subject:** Computer Networks
- **Institution:** *Vellore Institute of Technology, Chennai*

### Developed By

| Name |
|------|
| P C Guhan |
| S S Kishore Kumar |

**Project Guide:** Prof. Swaminathan Annadurai

---

## License

This project is developed for academic purposes.
