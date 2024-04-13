from pydantic import BaseModel,EmailStr

# class UserRole(str, Enum):
#     admin = "admin"
#     user = "user"
    

# class UserAuthAttribute(AuthAttribute):
#     def get_auth_value(self):
#         return self.auth_value

# @configure_permissions(
#     # Définition des rôles et autorisations
#     UserAuthAttribute(),
#     Allow(UserRole.admin, "manage"),
#     Allow(UserRole.user, "view"),
# )
# class UserPermission:
#     auth_value = "permissions"


class User(BaseModel):
    username: str
    name:str
    country: str
    phone:str
    adress:str
    email:EmailStr
    password:str
    # role: UserRole
    

    
def ResponseModel(data, status_code,message):
    return {
        "data": [data],
        "code": status_code,
        "message": message,
    }



def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

