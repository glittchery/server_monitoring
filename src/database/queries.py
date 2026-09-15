from src.database.database import session_factory, Base, engine
from src.database.models import Users, Monitors, Checks
from sqlalchemy import select, delete
from datetime import datetime, timedelta, UTC


class OrmQueries():
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            # engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            # engine.echo = True

#       USERS

    @staticmethod
    async def insert_user(username, password_hash):
        async with session_factory() as session:
            new_user = Users(username=username, password_hash=password_hash)
            session.add(new_user)
            await session.flush()
            user_id = new_user.id
            await session.commit()
            return user_id

    @staticmethod
    async def select_user(user_id):
        async with session_factory() as session:
            result = await session.get(Users, user_id)
            return result

    @staticmethod
    async def select_user_id(username):
        async with session_factory() as session:
            query = (
                select(Users.id)
                .where(Users.username == username)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(user_id):
        async with session_factory() as session:
            user = await session.get(Users, user_id)
            await session.delete(user)
            await session.commit()

    @staticmethod
    async def update_user(user_id, new_username, new_password_hash):
        async with session_factory() as session:
            user = await session.get(Users, user_id)
            if new_username is not None:
                user.username = new_username
            if new_password_hash is not None:
                user.password_hash = new_password_hash
            await session.commit()

#     MONITORS

    @staticmethod
    async def insert_monitor(user_id, type_of_request, name, url, interval):
        async with session_factory() as session:
            new_monitor = Monitors(user_id=user_id, type_of_request=type_of_request,
                                   name=name, url=str(url), interval=interval,
                                   next_check_at=datetime.now(UTC).replace(microsecond=0)
                                                 + timedelta(minutes=interval)
            )
            session.add(new_monitor)
            await session.commit()

    @staticmethod
    async def select_user_monitors(user_id):
        async with session_factory() as session:
            query = (
                select(Monitors)
                .where(Monitors.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def select_monitor(monitor_id):
        async with session_factory() as session:
            result = await session.get(Monitors, monitor_id)
            return result

    @staticmethod
    async def get_monitors_to_check():
        async with session_factory() as session:
            query = (
                select(Monitors)
                .where(Monitors.next_check_at <= datetime.now(UTC))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def delete_monitor(monitor_id):
        async with session_factory() as session:
            monitor = await session.get(Monitors, monitor_id)
            await session.delete(monitor)
            await session.commit()

    @staticmethod
    async def monitor_checktime_change(monitor_id, next_check_at):
        async with session_factory() as session:
            monitor = await session.get(Monitors, monitor_id)
            monitor.next_check_at = next_check_at
            await session.commit()

    @staticmethod
    async def change_monitor(monitor_id, new_name, new_url, new_interval):
        async with session_factory() as session:
            monitor = await session.get(Monitors, monitor_id)
            if new_name is not None:
                monitor.name = new_name
            if new_url is not None:
                monitor.url = str(new_url)
            if new_interval is not None:
                monitor.interval = new_interval
            await session.commit()

#     CHECKS

    @staticmethod
    async def insert_check_log(monitor_id, status_code, response_time, success, reason):
        async with session_factory() as session:
            check_log = Checks(
                monitor_id=monitor_id, status_code=status_code, response_time_ms=response_time,
                success=success, reason=reason)
            session.add(check_log)
            await session.commit()

    @staticmethod
    async def select_check_logs(monitor_id, period_start, period_end):
        async with session_factory() as session:
            query = (
                select(Checks)
                .where(Checks.monitor_id == monitor_id,
                       period_start <= Checks.created_at,
                       Checks.created_at <= period_end)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def delete_logs(monitor_id, period_start, period_end):
        async with session_factory() as session:
            query = (
                delete(Checks)
                .where(Checks.monitor_id == monitor_id,
                       period_start <= Checks.created_at,
                       Checks.created_at <= period_end)
            )
            await session.execute(query)
            await session.commit()
