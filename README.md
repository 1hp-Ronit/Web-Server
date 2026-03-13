# Python Web Server from Scratch

A working HTTP web server built using raw Python sockets. No Flask. No frameworks. Every line written by hand.

Built to understand what actually happens when a browser makes a request — TCP connections, HTTP parsing, routing, file serving — at every layer.

## What it does

- Accepts TCP connections on a configurable port
- Parses raw HTTP requests — method, path, headers, body
- Routes requests by method and path
- Serves static HTML files
- Returns correct status codes — 200, 404, 405, 500
- Handles client disconnections and errors gracefully

## Project structure

```
web-server/
    server.py        — main server loop and socket setup
    pages/
        index.html   — homepage
        about.html   — about page
        404.html     — not found page
```

## Run it

```bash
python server.py
```

Then open `http://localhost:8080` in your browser or test with curl:

```bash
curl -v http://localhost:8080/
curl -v http://localhost:8080/about
curl -v http://localhost:8080/doesnotexist
curl -v -X POST http://localhost:8080/
```

## What I learned

- How TCP connections work and what the three-way handshake actually does
- What an HTTP request and response look like at the byte level
- How sockets work as the boundary between application code and the OS
- Why frameworks like Flask exist and what they are doing underneath
- How DNS, ports, packets, and latency all fit together

## Planned features

- Static file serving with correct MIME types
- Threading to handle multiple clients simultaneously
- Query string parsing
- HTTPS / TLS
- Keep-alive connections
- Logging

## Why

I was using HTTP libraries in Python and Flutter without understanding what was happening. So I went all the way down and built it from scratch to prove I understood it.