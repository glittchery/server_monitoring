from src.database.queries import OrmQueries as orm
from argon2 import PasswordHasher

class AuthService():
    @staticmethod
    async def get_user(user_id):
        result = await orm.select_user(user_id)
        return result

    @staticmethod
    async def get_user_id(username):
        result = await orm.select_user_id(username)
        return result

    @staticmethod
    async def insert_user(username, password):
        ph = PasswordHasher()
        password_hash = ph.hash(password)
        user_id = await orm.insert_user(username, password_hash)
        return user_id

    @staticmethod
    async def log_in(username, password):
        user_id = await AuthService.get_user_id(username)
        result = await AuthService.get_user(user_id)
        ph = PasswordHasher()
        if result.username == username and result.password_hash == ph.hash(password):
            return {"success": True, "user_id": user_id}
        return {"success": False}
