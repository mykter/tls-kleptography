#!/usr/bin/env python3

import ssl
import http.server
import argparse

PORT = 4443

def serve(port, cert, key):
    httpd = http.server.HTTPServer(('localhost', port), http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        certfile=cert,
        keyfile=key,
        server_side=True,
        ssl_version=ssl.PROTOCOL_TLSv1_2) # Requires Python 2.7.9+
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serve a basic website over HTTPS.')
    parser.add_argument('cert', help='Certificate file for the site.')
    parser.add_argument('key', help='Private key file for the certificate.')
    parser.add_argument('--port', type=int, default=PORT, help='Port to serve on')
    args = parser.parse_args()

    serve(args.port, args.cert, args.key)
