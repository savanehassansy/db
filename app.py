from fastapi import FastAPI
from controllers.user_controllers import router as UserRouter
app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user") 

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenue to this fantastic app!"}