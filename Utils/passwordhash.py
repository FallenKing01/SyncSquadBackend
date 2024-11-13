import bcrypt
from Domain.extensions import salt

def hash_password(password):


    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(input_password, stored_password_hash):

    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password_hash.encode('utf-8'))
