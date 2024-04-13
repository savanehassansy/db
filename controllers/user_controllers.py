from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from datetime import timedelta

from services.user_services import (
    add_user,
    all_users,
    get_user,
    delete_user
)
from models import (
    User,
    ResponseModel,
    ErrorResponseModel,
)
from utils import (
    authenticate_user,
    create_access_token,
    check_phone_numbers,
    is_password_strong
)

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    user_info = {
        "username": user.username,
        "name": user.name,
        "phone": user.phone,
        "adress": user.adress,
        "country": user.country,
        "email": user.email
    }
    # création d'un JWT avec une durée d'expiration
    # Durée d'expiration de 30 minutes
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_info}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", }


@router.post("/", response_description="utilisateur créer")
async def add_user_data(user: User = Body(...)):
    try:
        print("try")
        # vérification du password
        if is_password_strong(user.password):
            # verification du numéo de téléphone
            if check_phone_numbers(user.phone):
                hashed_password = bcrypt_context.hash(user.password)
                user.password = hashed_password
                user = jsonable_encoder(user)
                new_user = await add_user(user)
                print("fin condition")
                return ResponseModel(new_user, status.HTTP_201_CREATED, "user ajouté avec succes.")
            else:
                return ResponseModel("", status.HTTP_400_BAD_REQUEST, "numéro de téléphone est inscorect")
        else:
            print("falss")
            return ResponseModel("", status.HTTP_400_BAD_REQUEST, "Le mot de passe doit être fort, avec au moins 8 caractères, une lettre majuscule, un chiffre et un caractère spécial.")
    except Exception as ex:
        return ex


@router.get("/users", response_description="tout les utilisateurs")
async def get_users(user: OAuth2PasswordRequestForm = Depends()):
    user = await all_users()
    if user:
        return ResponseModel(user, status.HTTP_200_OK, "liste des users")
    return ResponseModel(user, status.HTTP_200_OK, "Rien pour le moment")


@router.get("/{id}", response_description=" utilisateur")
async def get_user_data(id):
    user = await get_user(id)
    if user:
        return ResponseModel(user, status.HTTP_200_OK, "donne reçu")
    return ErrorResponseModel("erreur", status.HTTP_400_BAD_REQUEST, "utilisateur n'existe pas")


@router.delete("/{id}", response_description="delete user")
async def delete(id):
    user = await delete_user(id)
    if user:
        return ResponseModel(
            "user with ID: {} removed".format(
                id), status.HTTP_200_OK, "user deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", status.HTTP_400_BAD_REQUEST, "user with id {0} doesn't exist".format(
            id)
    )
