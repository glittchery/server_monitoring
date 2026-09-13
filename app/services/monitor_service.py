from app.database.queries import OrmQueries as orm


async def create_monitor(user_id, name, url):
    await orm.insert_monitor(user_id, name, url)


async def get_user_monitors(user_id):
    result = await orm.select_user_monitors(user_id)
    return result

async def update_monitor(monitor_id, new_name, new_url):
    await orm.change_monitor(monitor_id, new_name, new_url)

async def delete_monitor(monitor_id):
    await orm.delete_monitor(monitor_id)

