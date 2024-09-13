"""
module for echo server
"""
import socket
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs


def enable_echo_server(host='127.0.0.1', port=5000):
    """function to eanble echo server and parse requests and form response"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server working on http://{host}:{port}", '\n')

        while True:
            # Get connection
            client_connection, client_address = server_socket.accept()
            print(f"Connection from {client_address} established.")
            with client_connection:
                # Get client request
                request = client_connection.recv(1024).decode("utf-8")
                print(request, '\n')

                if not request:
                    continue

                # Split request by path an method
                request_strings = request.splitlines()
                request_string = request_strings[0].split()
                http_method = request_string[0]
                path = request_string[1]

                # Parse URL
                parsed_url = urlparse(path)
                query_params = parse_qs(parsed_url.query)
                status_code = query_params.get('status', ['200'])[0]

                if not status_code.isdigit() or int(status_code) not in [a.value for a in HTTPStatus]:
                    status_code = '200'

                status_message = HTTPStatus(int(status_code)).phrase

                # Form response
                headers = "\r\n".join(
                    f"{line.split(':')[0]}: {line.split(':')[1].strip()}"
                    for line in request_strings[1:] if ':' in line
                )

                response_message = (
                    f"Request Method: {http_method}\r\n"
                    f"Request Source: {client_address}\r\n"
                    f"Response Status: {status_code} {status_message}\r\n"
                    f"{headers}\r\n"
                )

                response = (f"HTTP/1.1 {status_code} {status_message}\r\n"
                            f"\r\n"
                            f"{response_message}")

                # Send response
                print(f"Sending response: {response}.")
                print("|-------------------------------------------------|")
                client_connection.sendall(response.encode("utf-8"))
                client_connection.close()


if __name__ == "__main__":
    enable_echo_server()
