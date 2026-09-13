from app.database.queries import OrmQueries as orm
from app.monitoring.requests import dns_request, https_request

async def perform_https_check(monitor_id):
    monitor = await orm.select_monitor(monitor_id)

    result = await https_request(monitor.url)

    await orm.insert_check_log(monitor.id, result["code"], result["response_time"], result["success"], result["reason"])

async def get_logs(monitor_id, start, end):
    logs = await orm.select_check_logs(monitor_id, start, end)
    return logs

async def delete_logs(monitor_id, start, end):
    await orm.delete_logs(monitor_id, start, end)
