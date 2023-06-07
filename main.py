from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from model import User, User_login
from database import MongoDB
import uvicorn

app = FastAPI()
security = HTTPBasic()

mongo = MongoDB('mongodb+srv://aistudio_3jo:a1234567@userdata.routxa4.mongodb.net/?retryWrites=true&w=majority', 'data')

@app.get('/userlist')
def load_user():
   user_list = mongo.load_user() 
   return {'result': user_list}

@app.post('/user')
def add_user(user: User):
    if mongo.add_user(user):
        return {'result', 'User added successfully'}
    else:
        raise HTTPException(status_code=400, detail='Adding user failed')

@app.post('/login')
def login(credentials: HTTPBasicCredentials):
    if mongo.check_user_cred(credentials.username, credentials.password):
        return {'result': 'Authentication succeeded'}
    else:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from fastapi.middleware.cors import CORSMiddleware

# from database import ( get_user_info, hash_password, verify_password )
# from model import UserLogin
# @app.post("/user/login")
# async def user_login(user:UserLoginSchema = Body(default=None)):
#     user_entered = jsonable_encoder(user)
#     user_info =  await get_user_info(user_entered["email"])
    
#     if await check_user(user_entered):
#         return {
#             "message" : "Successfully Logged In!",
#             "data": {    
#                 "access_token" :signJWT(user.email),
#                 "user_info": {
#                     "user_name": user_info["email"].split("@")[0],
#                     "profile_image": user_info["profile_image"],
#                     "role": user_info["role"]
#                 }
#             }
#         }
#     else:
#         raise HTTPException(status_code=400, detail="Incorrect password")


# async def check_user(user_entered):
#     try:
#         user_info = await get_user_info(user_entered["email"])
#         hashed_password = user_info["password"]
        
#         if verify_password(user_entered['password'], hashed_password):
#             return True
#         else:
#             return False
#     except:
#         raise HTTPException(status_code=400, detail="Incorrect email")