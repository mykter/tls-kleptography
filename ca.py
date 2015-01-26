#!/usr/bin/env python2

import os
import argparse

import rsabd # Python 2 support only

CA_CERT = "ca.crt"
CA_KEY = "ca.key"
REQ = "req.csr"

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='A mini-ca to generate backdoor-ed RSA keys.')
    parser.add_argument('domain', help='Domain to generate a private key and certificate for.')
    args = parser.parse_args()

    server_key = args.domain + ".key"
    server_cert = args.domain + ".crt"

    # Generate a backdoor-ed key if we haven't already:
    if not os.path.isfile(server_key):
        with open(server_key, "w") as pk:
            pk.write(rsabd.generate_new_key().exportKey())

    # Generate a server certificate from the private key if we haven't already
    if not os.path.isfile(server_cert):
        os.system("openssl req -new -key {} -out {}".format(server_key, REQ))
        os.system("openssl x509 -req -in {} -CA {} -CAkey {} -CAcreateserial -out {}".format(REQ, CA_CERT, CA_KEY, server_cert))
        os.unlink(REQ)
