from app.database.database import session_factory, Base
from argon2 import PasswordHasher

class Orm():
    @staticmethod
    def create_tables():
        Base.metadata.create_all(async_engine)

    async def insert_user(self, name, password):
        async with session_factory() as session:
            ph = PasswordHasher()
            new_user = Users(username=name, password=ph.hash(password))
            session.add(new_user)
            session.commit()
            