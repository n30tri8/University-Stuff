# import socket programming library 
import socket
# import thread module
from _thread import *
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken
import datetime


# ----------------------------
physical_cs = None

# ----------------------------


def do_encrypt(cipher_suite, message):
    cipher_text = cipher_suite.encrypt(message)
    return cipher_text


def do_decrypt(cipher_suite, cipher_text):
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text


def init():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)  # The key is type bytes still
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


def init_session(c):
    # init session
    print('trying to start new session with client')
    session_cs_l = None
    session_expiration_l = None
    valid_parse_l = True
    data_l = c.recv(1024)
    if not data_l:
        print('nothing got from client')
        valid_parse_l = False
    try:
        data_l = str(do_decrypt(physical_cs, data_l).decode('ascii'))
    except InvalidToken:
        print('invalid cipher suites')
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
                data_l = do_encrypt(physical_cs, data_l)
                c.send(data_l)
                session_cs_l = generate_session_key(password_provided)
            except ValueError:
                valid_parse_l = False

        else:
            valid_parse_l = False
    else:
        print('wrong physical key')
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
            data = c.recv(1024)
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
            content += data
            data = "send next".encode('ascii')
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
    # print_lock = threading.Lock()
    physical_cs = init()
    Main()