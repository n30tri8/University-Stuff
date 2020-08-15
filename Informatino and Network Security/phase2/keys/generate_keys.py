from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# Generating server key
private_key_server = rsa.generate_private_key(public_exponent=65537,
        key_size=8192,
        backend=default_backend()
    )
public_key_server = private_key_server.public_key()

# Storing server key
pem = private_key_server.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
with open('private_key_server.pem', 'wb') as f:
    f.write(pem)
pem = public_key_server.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
with open('public_key_server.pem', 'wb') as f:
    f.write(pem)


# Generating client key
private_key_client = rsa.generate_private_key(public_exponent=257,
        key_size=8192,
        backend=default_backend()
    )
public_key_client = private_key_client.public_key()

# Storing client key
pem = private_key_client.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
with open('private_key_client.pem', 'wb') as f:
    f.write(pem)
pem = public_key_client.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
with open('public_key_client.pem', 'wb') as f:
    f.write(pem)