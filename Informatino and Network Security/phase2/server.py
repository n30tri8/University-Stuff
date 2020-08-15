# import socket programming library 
import socket
# import thread module
from _thread import *
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
import datetime


# ----------------------------
public_key_self = None
private_key_self = None
public_key_client = None
signature_delimeter = b'=={(SIGN COMES BELOW)}=='

# ----------------------------


def do_encrypt(cipher_suite, message):
    cipher_text = cipher_suite.encrypt(message)
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
    public_key_client_l = None
    with open(".\\keys\\private_key_server.pem", "rb") as key_file:
        private_key_self_l = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    with open(".\\keys\\public_key_server.pem", "rb") as key_file:
        public_key_self_l = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    with open(".\\keys\\public_key_client.pem", "rb") as key_file:
        public_key_client_l = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return private_key_self_l, public_key_self_l, public_key_client_l


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


def init_session(c):
    # init session
    print('trying to start new session with client')
    session_cs_l = None
    session_expiration_l = None
    valid_parse_l = True
    data_l = c.recv(2048)
    if not data_l:
        print('nothing got from client')
        valid_parse_l = False
    try:
        print('before dec init')
        data_l = do_decrypt_rsa(private_key_self, data_l)
        valid_sign, data_l = verify_message_sign(data_l)
        if valid_sign:
            data_l = str(data_l.decode('ascii'))
            print('signature verified')
        else:
            print('signature not verfied')
            valid_parse_l = False
            data_l = 'invalid signature'.encode('ascii')
            data_l = do_encrypt_rsa(public_key_client, data_l)
            c.send(data_l)
            return valid_parse_l, None, None
    except InvalidToken:
        valid_parse_l = False
        return valid_parse_l, None, None
    except ValueError:
        valid_parse_l = False
        return valid_parse_l, None, None
    
    if data_l.startswith('session key is:\n'):
        nl1 = data_l.find('\n') + 1
        nl2 = data_l[nl1:].find('\n') + nl1
        if nl2 != -1:
            password_provided = data_l[nl1:nl2]
            try:
                expire = float(data_l[nl2 + 1:])
                session_expiration_l = datetime.datetime.now() + datetime.timedelta(seconds=expire)
                data_l = 'accepted, do continue'.encode('ascii')
                data_l = sign_message(data_l)
                assert(len(data_l) <= 1024)
                data_l = do_encrypt_rsa(public_key_client, data_l)
                c.send(data_l)
                session_cs_l = generate_session_key(password_provided)
            except ValueError:
                valid_parse_l = False

        else:
            valid_parse_l = False
    else:
        print('wrong rsa cryptography key')
        valid_parse_l = False

    return valid_parse_l, session_cs_l, session_expiration_l


# thread fuction
def threaded(c, addr):
    content = bytes()
    continue_con = True
    while continue_con:
        # init session
        valid_parse, session_cs, session_expiration = None, None, None
        for i in range(3):
            valid_parse, session_cs, session_expiration = init_session(c)

            if valid_parse:
                print('new session established')
                continue_con = True
                break
            else:
                print('session could not start, Bye')
                continue_con = False
                # data = "init session again. key expired".encode('ascii')
                # data = do_encrypt(session_cs, data)
                # c.send(data)

        # session established. continue connection
        while (session_expiration - datetime.datetime.now()).days >= 0 and continue_con:
            # data received from client
            data = c.recv(2048)
            if not data:
                print('Bye')
                continue_con = False
                break
            if not ((session_expiration - datetime.datetime.now()).days >= 0):
                data = "init session again. key expired".encode('ascii')
                data = do_encrypt(session_cs, data)
                c.send(data)
                break
            data = do_decrypt(session_cs, data)
            valid_sign, data = verify_message_sign(data)
            if valid_sign:
                print('MAC verified')
            else:
                print('MAC not verfied')
                break
            content += data
            data = "send next".encode('ascii')
            data = sign_message(data)
            data = do_encrypt(session_cs, data)
            c.send(data)

    # connection closed
    c.close()
    f = open('.\\got_from_client_' + addr[0] + '.txt', 'wb')
    f.write(content)


def Main():
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode 
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit 
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client 
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # print_lock.release()
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c, addr))

    s.close()


if __name__ == '__main__':
    private_key_self, public_key_self, public_key_client = init()
    Main()