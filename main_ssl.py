#!/bin/env python3

from website import create_app
import ssl

app = create_app()

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain("server_certificate.pem", "server_privatekey.pem")
    
    app.run(debug=True, host="0.0.0.0", port=5443, ssl_context=ssl_context)
