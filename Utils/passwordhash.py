import bcrypt
from Domain.extensions import salt

def hash_password(password):


    return bcrypt.hashpw(password.encode('utf-8'), salt)