import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', 8080))

server.listen(5)



def read_request(client : socket.socket) -> tuple[str, bytes]:    
    raw = b''
    while b'\r\n\r\n' not in raw:
        chunk = client.recv(4096)
        if not chunk:
            raise ConnectionError("Client disconnected before sending complete headers")
        raw += chunk
        
    headers_end = raw.find(b'\r\n\r\n')
    headers_raw = raw[:headers_end].decode('utf-8') # decoding the header
    
    # Checking method
    request_line = headers_raw.split('\r\n')[0]
    method = request_line.split(' ')[0]
    
    if method in ('GET', 'DELETE', 'HEAD', 'OPTIONS'):
        return headers_raw, b''
    body_so_far = raw[headers_end+4:] # body that might be received in the chunk with the header ending
    
    # Parse content length from header
    
    content_length = 0
    for line in headers_raw.split('\r\n')[1:]:
        if line.lower().startswith('content-length:'):
            content_length = int(line.split(': ', 1)[1].strip())
            break    
    if content_length == 0:
        return headers_raw, b''
        
    while (len(body_so_far)<content_length):
        chunk = client.recv(4096)
        if not chunk:
            break
        body_so_far += chunk
    return headers_raw, body_so_far[:content_length]
try:
    while True:
        client, address = server.accept()
        try:
            headers_raw, body = read_request(client=client)
            print(headers_raw)
        
            response = b"HTTP/1.1 200 OK\r\nContent-Length:18\r\nContent-Type: text/plain\r\n\r\nReading successful"
            client.sendall(response)
        except ConnectionError as e: # if client disconnects before sending all the headers
            print(f"Connection error {e}")
        except BrokenPipeError:
            print("Client disconnected mid-respone")
        except ConnectionResetError:
            print(f"Client {address} reset the connection")
        
        finally:
            client.close()
except KeyboardInterrupt:
    print("Closing the Server...")
finally:
    server.close()
        
        