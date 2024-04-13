import motor.motor_asyncio
from datetime import datetime, timedelta
import jwt
from config import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext
import phonenumbers


from models import (
    User,
    
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modèle Pydantic pour les informations d'authentification 
async def authenticate_user(username: str, password: str):
    # Connexion à la base de données MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:27017/")
    database = client.user
    users_collection = database.get_collection("users_collection")
    user_data = await users_collection.find_one({"username": username})
    if user_data:
        user = User(**user_data)
        if bcrypt_context.verify(password, user.password):
            return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_password_strength(password):
    if (
        len(password) < 8 or
        not any(char.isupper() for char in password) or
        not any(char.isdigit() for char in password) or
        not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password)
    ):
        raise ValueError(
            "Le mot de passe doit être fort, avec au moins 8 caractères, une lettre majuscule, un chiffre et un caractère spécial.")
    return password


def is_password_strong(password):
    try:
        validate_password_strength(password)
        return True
    except ValueError:
        return False


def check_phone_numbers(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberFormatException:
        print("Format de numéro de téléphone incorrect.")

