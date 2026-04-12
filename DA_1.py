import socket
import ssl
import time
from urllib.parse import urlparse


def download(url: str):
    steps = []

    def log(step, text, type="info"):
        steps.append({"step": step, "text": text, "type": type})

    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"

    log("Step 1", "URL Parsing", "step")
    log("URL", f"Scheme  : {parsed.scheme}", "ok")
    log("URL", f"Host    : {host}", "ok")
    log("URL", f"Port    : {port}", "ok")
    log("URL", f"Path    : {path}", "ok")

    log("Step 2", "DNS Resolution", "step")
    log("DNS", f"Querying DNS for '{host}' ...", "info")
    t0 = time.perf_counter()
    results = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    dns_time = (time.perf_counter() - t0) * 1000
    for r in results:
        ip = r[4][0]
        family = "AF_INET6" if r[0] == socket.AF_INET6 else "AF_INET"
        log("DNS", f"Resolved : {ip} (family={family})", "ok")
    chosen = results[0][4][0]
    log("DNS", f"DNS query took {dns_time:.1f} ms", "ok")
    log("DNS", f"Using    : {chosen}", "info")

    log("Step 3", "TCP 3-Way Handshake", "step")
    family, socktype, proto, _, sockaddr = results[0]
    sock = socket.socket(family, socktype, proto)
    sock.settimeout(10)
    log("TCP", f"Connecting to {chosen}:{port}", "info")
    t0 = time.perf_counter()
    sock.connect(sockaddr)
    rtt = (time.perf_counter() - t0) * 1000
    log("TCP", "-> Sending SYN", "info")
    log("TCP", "<- Received SYN-ACK", "ok")
    log("TCP", "-> Sent ACK", "ok")
    log("TCP", f"Connection established. RTT ~ {rtt:.1f} ms", "ok")

    if parsed.scheme == "https":
        log("Step 4", "TLS Handshake", "step")
        ctx = ssl.create_default_context()
        tls = ctx.wrap_socket(sock, server_hostname=host)
        log("TLS", f"Version       : {tls.version()}", "ok")
        log("TLS", f"Cipher        : {tls.cipher()[0]}", "ok")
        cert = tls.getpeercert()
        log("TLS", f"Cert valid to : {cert.get('notAfter')}", "ok")
        conn = tls
    else:
        conn = sock
        log("Step 4", "TLS Handshake", "step")
        log("TLS", "Skipped (HTTP)", "warn")

    log("Step 5", "HTTP GET Request", "step")
    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    conn.sendall(req.encode())
    log("HTTP", f"GET {path} HTTP/1.1", "info")
    log("HTTP", f"Host: {host}", "info")
    log("HTTP", "Connection: close", "info")

    log("Step 6", "HTTP Response", "step")
    raw = b""
    t0 = time.perf_counter()
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        raw += chunk
    elapsed = (time.perf_counter() - t0) * 1000
    conn.close()

    log("RESPONSE", f"Received {len(raw):,} bytes in {elapsed:.1f} ms", "ok")
    try:
        text = raw.decode("utf-8", errors="ignore")
        lines = text.split("\n")
        log("RESPONSE", f"Status : {lines[0].strip()}", "ok")
        log("RESPONSE", "--- Response Headers ---", "info")
        for line in lines[1:]:
            line = line.strip()
            if not line:
                break
            if ":" in line:
                log("HEADER", line, "info")
    except:
        log("RESPONSE", "Decode failed", "warn")

    return steps
