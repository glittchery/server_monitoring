from argon2.exceptions import VerifyMismatchError

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
        if user_id is None:
            return {"success": False}
        result = await AuthService.get_user(user_id)
        ph = PasswordHasher()
        try:
            ph.verify(result.password_hash, password)
        except VerifyMismatchError:
            return {"success": False}

        return {"success": True, "user_id": user_id}


    @staticmethod
    async def update_user(user_id, new_username, new_password):
        ph = PasswordHasher()
        await orm.update_user(user_id, new_username, ph.hash(new_password))

    @staticmethod
    async def delete_user(user_id):
        await orm.delete_user(user_id)
