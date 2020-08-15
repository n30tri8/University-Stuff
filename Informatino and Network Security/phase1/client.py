# Import socket module 
import socket
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
import random
import string
import datetime
from math import ceil
import time

# ----------------------------
physical_cs = None
session_cs = None
packet_length = 512
# ----------------------------


def do_encrypt(cipher_suite, plaintext):
    cipher_text = cipher_suite.encrypt(plaintext)
    return cipher_text


def do_decrypt(cipher_suite, cipher_text):
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text


def init():
    file = open('key.key', 'rb')
    key = file.read() # The key will be type bytes
    file.close()
    cipher_suite = Fernet(key)
    return cipher_suite


def generate_session_key(password_provided):
    password = password_provided.encode()  # Convert to type bytes
    salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    cipher_suite = Fernet(key)
    return cipher_suite


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def init_session(s):
    # initialize session
    session_cs_l = None
    session_expiration_l = 20
    valid_parse_l = False
    password_provided = random_string()
    m = "session key is:\n" + password_provided + '\n' + str(session_expiration_l)
    m = do_encrypt(physical_cs, m.encode('ascii'))
    i = 0
    while i < 10:  # try 10 time to init session
        s.send(m)
        data = s.recv(1024)
        try:
            res = str(do_decrypt(physical_cs, data).decode('ascii'))
            if res == "accepted, do continue":
                session_cs_l = generate_session_key(password_provided)
                session_expiration_l = datetime.datetime.now() + datetime.timedelta(seconds=session_expiration_l)
                valid_parse_l = True
                break
        except InvalidToken:
            valid_parse_l = False

    return valid_parse_l, session_cs_l, session_expiration_l


def Main():
    content = None
    no_packets = None
    cu_packet = 0
    ans = input('\nfile to send or "no":\n')
    if ans != 'no':
        f = open(ans, "rb")
        content = f.read()
        f.close()
        no_packets = ceil(len(content) / float(packet_length))
    else:
        no_packets = 0
        return

    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while cu_packet < no_packets:
        # initialize session
        valid_parse, session_cs, session_expiration = init_session(s)
        if not valid_parse:
            print('session could not start, Exiting')
            break

        # send payload
        while ((session_expiration - datetime.datetime.now()).days >= 0) and cu_packet < no_packets:
            start = cu_packet * packet_length
            end = start + packet_length
            message = content[start:end]
            message = do_encrypt(session_cs, message)
            s.send(message)
            # print('sent to server:', str(do_decrypt(session_cs, message).decode('ascii')))
            data = s.recv(1024)
            try:
                data = str(do_decrypt(session_cs, data).decode('ascii'))
            except InvalidToken:
                print('error in decrypting message, expected session_cs')
                break
            print('Received from the server :', data)
            if data == "send next":
                cu_packet += 1
            elif data.startswith('init session again. key expired'):
                break
            else:
                break
            time.sleep(1)

    # close the connection 
    s.close()


if __name__ == '__main__':
    physical_cs = init()
    Main() 