from src.database.queries import OrmQueries as orm
from src.monitoring.requests import dns_request, https_request
from src.database.models import dns_or_https


async def perform_https_check(monitor_id, url):
    result = await https_request(url)
    if not result["success"]:
        await orm.insert_check_log(monitor_id, None, None, result["success"], result["reason"])
    else:
        await orm.insert_check_log(monitor_id, result["code"], result["response_time"], result["success"], result["reason"])


async def perform_dns_check(monitor_id, dns_resolver, url):
    result = await dns_request(dns_resolver, url)
    if not result["success"]:
        await orm.insert_check_log(monitor_id, None, None, result["success"], result["reason"])
    else:
        await orm.insert_check_log(monitor_id, result["code"], result["response_time"], result["success"], result["reason"])


class CheckService():
    @staticmethod
    async def perform_check(monitor_id, user_id):
        monitor = await orm.select_monitor(monitor_id)
        if monitor.user_id != user_id:
            return {"success": False,
                    "status_code": 404,}
        if monitor.type_of_request == dns_or_https.https:
            await perform_https_check(monitor.id, monitor.url)
        else:
            domain_list = [
                "youtube.com",
                "yandex.ru",
                "microsoft.com",
                "ozon.ru",
                "spotify.com"
            ]
            for domain_name in domain_list:
                await perform_dns_check(monitor.id, monitor.url, domain_name)
        return {"success": True,
                "status_code": 200}


    @staticmethod
    async def get_logs(monitor_id, start, end, user_id):
        monitor = await orm.select_monitor(monitor_id)
        if monitor.user_id != user_id:
            return {"success": False,
                    "status_code": 404}
        logs = await orm.select_check_logs(monitor_id, start, end)
        return {"success": True,
                "logs": logs}

    @staticmethod
    async def delete_logs(monitor_id, start, end, user_id):
        monitor = await orm.select_monitor(monitor_id)
        if monitor.user_id != user_id:
            return {"success": False,
                    "status_code": 404}
        await orm.delete_logs(monitor_id, start, end)
        return {"success": True,
                "status_code": 200}
