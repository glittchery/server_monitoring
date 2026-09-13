import time
import requests


#                                        РУЧНЫЕ ЗАПРОСЫ
# def http_request(url: str, port: int):
#     start = time.perf_counter()
#     sock = socket.create_connection((url, port))
#     request = (
#         "GET / HTTP/1.1\r\n"
#         f"Host: {url} \r\n"
#         "Connection: close\r\n"
#         "\r\n"
#     )
#     sock.sendall(request.encode())
#     response = sock.recv(4096).decode()
#     sock.close()
#     elapsed = (time.perf_counter() - start) * 1000
#     return [response.split("\r\n")[0], elapsed]
#
# def https_request(url: str, port: int):
#     start = time.perf_counter()
#     sock = socket.create_connection((url, port)) #.socket + .connect
#     context = ssl.create_default_context()
#     sock = context.wrap_socket(sock, server_hostname=url)
#     request = (
#         "GET / HTTP/1.1\r\n"
#         f"Host: {url} \r\n"
#         "Connection: close\r\n"
#         "\r\n"
#     )
#     sock.sendall(request.encode())
#     response = sock.recv(4096).decode()
#     sock.close()
#     elapsed = (time.perf_counter() - start) * 1000
#     return [response.split("\r\n")[0], elapsed]
#
#
# while 1:
#     data = input()
#     if data == "0":
#         break
#     url, port = data.split()
#     port = int(port)
#     if port == 80:
#         test = http_request(url, port)
#         print(f"{url:30}" f"{test[0]} " f"{test[1]:.0f} ms")
#     elif port == 443:
#         test = https_request(url, port)
#         print(f"{url:30}" f"{test[0]} " f"{test[1]:.0f} ms")



def https_request(url: str):
    try:
        start = time.perf_counter()
        response = requests.get(url, timeout=5)
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "code": response.status_code,
            "response_time": f"{elapsed} ms",
            "success": response.status_code == 200,
            "reason": response.reason,
        }
    except requests.RequestException as error:
        return {
            "success": False,
            "reason": f"{error}",
        }

def dns_request(dns_resolver: str, url: str):
    try:
        start = time.perf_counter()
        response = requests.get(
            dns_resolver,
            params={
                "name": url,
                "type": "A",
            },
            headers={
                "Accept": "application/dns-json",
            },
            timeout=10,
        )
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "code": response.status_code,
            "response_time": elapsed,
            "success": response.status_code == 200,
            "reason": response.reason,
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "reason": f"{error}",
        }

# if __name__ == "__main__":
#     defdns = "https://cloudflare-dns.com/dns-query"
#     defurl = "https://google.com"
#     while 1:
#         request = input("Select the request type: ")
#         if request == "https":
#             url = input("URL address: ")
#             print(https_request(url if len(url) else defurl)["response"])
#         elif request == "dns":
#             dns_resolver = input("DNS server: ")
#             url = input("URL address: ")
#             print(dns_request(dns_resolver if len(dns_resolver) else defdns, url if len(url) else defurl)["response"])
#
#






