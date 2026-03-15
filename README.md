# Python Web Server from Scratch

A multithreaded HTTP web server built using raw Python sockets. No Flask. No frameworks. Every line written by hand.

Built to understand what actually happens when a browser makes a request — TCP connections, HTTP parsing, routing, file serving, threading — at every layer.

## What it does

- Accepts TCP connections on a configurable port
- Handles multiple clients simultaneously with threading
- Parses raw HTTP requests — method, path, headers, body
- Routes requests by method and path
- Serves static files with correct MIME types
- Detects and blocks path traversal attacks
- URL decodes paths before processing
- Returns correct status codes — 200, 403, 404, 405
- Handles client disconnections and errors gracefully
- Closes every socket cleanly with finally blocks

## Project structure

```
web-server/
    server.py        — main loop, socket setup, threading
    mime_types.py    — extension to content type mapping
    README.md
    pages/
        index.html   — homepage
        about.html   — about page
        404.html     — not found page
        style.css    — stylesheet
```

## Run it

```bash
python server.py
```

Then open `http://localhost:8080` in your browser or test with curl:

```bash
# Basic requests
curl.exe -v http://localhost:8080/
curl.exe -v http://localhost:8080/about
curl.exe -v http://localhost:8080/doesnotexist

# Method handling
curl.exe -v -X POST http://localhost:8080/

# Security — path traversal attempts
curl.exe http://localhost:8080/%2e%2e%2fserver.py
curl.exe http://localhost:8080/../server.py
```

## What I learned

- How TCP connections work and what the three-way handshake actually does
- What an HTTP request and response look like at the byte level
- How sockets work as the boundary between application code and the OS
- What file descriptors are and why closing them matters
- How MIME types work and why Content-Type affects browser behaviour
- How path traversal attacks work and how to block them
- How threading lets a server handle multiple clients simultaneously
- Why frameworks like Flask exist and what they are doing underneath
- How DNS, ports, packets, and latency all fit together

## Security

- Path traversal protection using `os.path.realpath()` — requests cannot escape the pages folder
- URL decoding before path resolution — encoded attacks like `%2e%2e%2f` are caught
- Unknown paths outside the pages folder return 403 Forbidden

## Why

I was using HTTP libraries in Python and Flutter without understanding what was happening. So I went all the way down and built it from scratch to prove I understood it.