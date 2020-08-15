# Import socket module 
import socket
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
import random
import string
import datetime
from math import ceil
import time

# ----------------------------
public_key_self = None
private_key_self = None
public_key_server = None
session_cs = None
packet_length = 512
signature_delimeter = b'=={(SIGN COMES BELOW)}=='

# ----------------------------


def do_encrypt(cipher_suite, plaintext):
    cipher_text = cipher_suite.encrypt(plaintext)
    return cipher_text


def do_decrypt(cipher_suite, cipher_text):
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text


def do_encrypt_rsa(public_key, plaintext):
    cipher_text = public_key.encrypt(plaintext, 
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return cipher_text


def do_decrypt_rsa(private_key, cipher_text):
    plain_text = private_key.decrypt(cipher_text,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )  
    return plain_text


def sign_message(message):
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash, default_backend())
    hasher.update(message)
    signature = hasher.finalize()
    return message + signature_delimeter + signature


def verify_message_sign(message_with_signature):
    valid_sign_l = True
    message_l = None
    try:
        m_splitted = message_with_signature.split(signature_delimeter)
        assert(len(m_splitted) == 2)
        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash, default_backend())
        hasher.update(m_splitted[0])
        new_signature = hasher.finalize()
        assert(new_signature == m_splitted[1])
        message_l = m_splitted[0]
    except AssertionError:
        valid_sign_l = False
    
    return valid_sign_l, message_l


def init():
    private_key_self_l = None
    public_key_self_l = None
    public_key_server_l = None
    with open(".\\keys\\private_key_client.pem", "rb") as key_file:
        private_key_self_l = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    with open(".\\keys\\public_key_client.pem", "rb") as key_file:
        public_key_self_l = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    with open(".\\keys\\public_key_server.pem", "rb") as key_file:
        public_key_server_l = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return private_key_self_l, public_key_self_l, public_key_server_l


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
    m = ("session key is:\n" + password_provided + '\n' + str(session_expiration_l)).encode('ascii')
    m = sign_message(m)
    assert(len(m) <= 1024)
    m = do_encrypt_rsa(public_key_server, m)
    i = 0
    while i < 10:  # try 10 time to init session
        s.send(m)
        data = s.recv(2048)
        try:
            res = do_decrypt_rsa(private_key_self, data)
            valid_sign, res = verify_message_sign(res)
            if valid_sign:
                res = str(res.decode('ascii'))
                print('signature verified')
            else:
                print('signature not verfied')
                valid_parse_l = False
                res = 'invalid signature'.encode('ascii')
                res = do_encrypt_rsa(public_key_server, res)
                s.send(res)
                return valid_parse_l, None, None

            if res == "accepted, do continue":
                session_cs_l = generate_session_key(password_provided)
                session_expiration_l = datetime.datetime.now() + datetime.timedelta(seconds=session_expiration_l)
                valid_parse_l = True
                break
        except InvalidToken:
            valid_parse_l = False
        except ValueError:
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
            print('currently sending [%d:%d]'%(start, end))
            message = content[start:end]
            message = sign_message(message)
            message = do_encrypt(session_cs, message)
            s.send(message)
            # print('sent to server:', str(do_decrypt(session_cs, message).decode('ascii')))
            data = s.recv(2048)
            try:
                data = do_decrypt(session_cs, data)
                valid_sign, data = verify_message_sign(data)
                if valid_sign:
                    data = str(data.decode('ascii'))
                    print('MAC verified')
                else:
                    print('MAC not verfied')
                    break
                
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
    private_key_self, public_key_self, public_key_server = init()
    Main() 