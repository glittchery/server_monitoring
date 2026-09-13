from app.database.database import session_factory, Base, engine
from argon2 import PasswordHasher
from app.database.models import Users, Monitors, Checks
import datetime

class OrmQueries():
    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)

#       USERS

    @staticmethod
    async def insert_user(username, password):
        async with session_factory() as session:
            ph = PasswordHasher()
            new_user = Users(username=username, password=ph.hash(password))
            await session.add(new_user)
            await session.commit()

    @staticmethod
    async def select_user(user_id):
        async with session_factory() as session:
            query = (
                select(Users.id)
                .where(Users.id == user_id)
            )
            result = await session.execute(query)
            return result

    @staticmethod
    async def delete_user(user_id):
        async with session_factory() as session:
            user = await session.get(Users, user_id)
            await session.delete(user)
            await session.commit()

    @staticmethod
    async def update_user(user_id, new_username, new_password):
        async with session_factory() as session:
            ph = PasswordHasher()
            user = await session.get(Users, user_id)
            user.username = new_username
            user.password_hash = ph.hash(new_password)
            await session.commit()

#     MONITORS

    @staticmethod
    async def insert_monitor(user_id, name, url):
        async with session_factory() as session:
            new_monitor = Monitors(user_id=user_id, name=name, url=url)
            await session.add(new_monitor)
            await session.commit()

    @staticmethod
    async def select_user_monitors(user_id):
        async with session_factory() as session:
            query = (
                select(Monitors)
                .where(Monitors.user_id == user_id)
            )
            result = await session.execute(query)
            return result

    @staticmethod
    async def select_monitor(monitor_id):
        async with session_factory() as session:
            result = await session.get(Monitors, monitor_id)
            return result

    @staticmethod
    async def delete_monitor(monitor_id):
        async with session_factory() as session:
            monitor = await session.get(Monitors, monitor_id)
            await sesion.delete(monitor)
            await session.commit()

    @staticmethod
    async def change_monitor(monitor_id, new_name, new_url):
        async with session_factory() as session:
            monitor = await session.get(Monitors, monitor_id)
            monitor.name = new_name
            monitor.url = new_url
            await session.commit()

#     CHECKS

    @staticmethod
    async def insert_check_log(monitor_id, status_code, response_time, success, reason):
        async with session_factory() as session:
            check_log = Checks(
                monitor_id=monitor_id, status_code=status_code, response_time=response_time,
                success=success, reason=reason)
            await session.add(check_log)
            await session.commit()

    @staticmethod
    async def select_check_logs(monitor_id, period_start, period_end):
        async with session_factory() as session:
            query = (
                select(Checks)
                .where((Checks.monitor_id == monitor_id) and (period_start <= Checks.created_at <= period_end))
            )
            result = await session.execute(query)
            return result

    @staticmethod
    async def delete_logs(monitor_id, period_start, period_end):
        async with session_factory() as session:
            query = (
                delete(Checks)
                .where((Checks.monitor_id == monitor_id) and (period_start <= Checks.created_at <= period_end))
            )
            await session.execute(query)
            await session.commit()
