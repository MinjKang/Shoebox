from pymongo import MongoClient
from model import User, User_login
import pydantic
from bson import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def load_user(self):
        user_data = self.db['users'].find()
        user_list = []
        for item in user_data:
            user_list.append(item)
        return user_list

    def check_user_cred(self, username: str, password: str) -> bool:
        return bool(self.db.users.find_one({'username': username, 'password': password}))

    def add_user(self, user: User) -> bool:
        try:
            self.db.users.insert_one(user.dict())
            return True
        except Exception:
            return False

    def update_size(self, id: int, brand: str, size: int):
        self.db['users'].update_one({'id': id}, {"$set": {"shoesSizes": {brand : size}}})
        user_data = self.db['users'].find_one({"userId": id})
        print(user_data)
        
        return user_data

# # MongoDB 연결
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:password@mongodb:27017')
# db = client.HGOO
# collection_users = db.users


# # password 암호화 모듈
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # password 비교
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# # password 암호화
# def hash_password(password):
#     return pwd_context.hash(password)


# # DB 에서 User 정보 가져오기
# async def get_user_info(user_email: str):
#     user_info = await collection_users.find_one({"email":user_email})
#     if user_info:
#         return user_info