import socket
import mime_types
import os
from urllib.parse import unquote
import threading

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


# Build response
def build_response(
    status_code: int,
    body: str | bytes,
    content_type: str = 'text/html; charset=utf-8',
    extra_headers: dict[str,str] | None = None) -> bytes:
    
    if isinstance(body, str):
        body_bytes = body.encode('utf-8')
    else:
        body_bytes = body
        
    status_phrases = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        500: 'Internal Server Error',
    }
    
    phrase = status_phrases.get(status_code, 'Unknown')
    
    # Creating the headers
    headers = (
        f"HTTP/1.1 {status_code} {phrase}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
    )
    if extra_headers: 
        for key, value in extra_headers.items():
            headers += f"{key}: {value}\r\n"
    headers += "\r\n"
    return headers.encode('utf-8') + body_bytes

def read_file(path: str) -> bytes:
        with open(path, 'rb') as f:
            data = f.read()
            return data
   

def parse_request(client : socket.socket) -> tuple[str, str, str, bytes]:
    """returns method, path, headers, body"""
    headers, body = read_request(client=client)
    status_line = headers.split('\r\n',1)[0]
    try: 
        method, path, version = status_line.split(' ')
        return method, path, headers, body
    except ValueError:
        raise ValueError(f"Malformed Request Line: {status_line}")  
    
def serve_static(path : str) -> bytes:
    path = unquote(path)
    if path == '/':
        path = '/index.html'  
    
    _, ext = os.path.splitext(path)
    if not ext:
        path = path+'.html'  
    pages_dir = os.path.realpath('pages')
    file_path = os.path.realpath(os.path.join('pages', path.lstrip('/')))
    if not file_path.startswith(pages_dir + os.sep):
        return build_response(status_code= 403, body='<h1>Forbidden</h1>') 
    
    try:
        response_body = read_file(file_path)
    except FileNotFoundError:
        try:
            response_body = read_file('pages/404.html')
            response = build_response(status_code=404, body=response_body)   
            return response
        except FileNotFoundError:
            return build_response(404, '<h1> Not Found </h1>')
            
    content_type = mime_types.get_content_type(file_path)
    
    return build_response(200, response_body, content_type)

    
    
def handle_request(method: str, path: str, headers: str, body: bytes) -> bytes:
    """Owns the method Check"""
    if method == 'GET':
        return serve_static(path)
    else:
        build_response(405, '')

def handle_client(client: socket.socket, address: tuple) -> None:
    try:
        method, path, headers, body = parse_request(client=client)
            # print(f"Method: {method}, Path: {path}")

        response = handle_request(method, path, headers, body)
        client.sendall(response)
    except ConnectionError as e: # if client disconnects before sending all the headers
        print(f"Connection error {e}")
    except BrokenPipeError:
        print("Client disconnected mid-respone")
    except ConnectionResetError:
        print(f"Client {address} reset the connection")
    except Exception as e:
        print(f"Exception: {e}")
        
    finally:
            client.close()

try:
    while True:
        client, address = server.accept()
        print(f"Connection from {address}")
        thread = threading.Thread(target = handle_client, args=(client, address))
        thread.daemon = True
        thread.start()
except KeyboardInterrupt:
    print("Closing the Server...")
finally:
    server.close()
        
        