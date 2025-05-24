openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout key.pem -out cert.pem -days 365 -config localhost.cf
openssl x509 -outform der -in cert.pem -out cert.crt
certutil -addstore Root cert.crt