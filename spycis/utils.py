import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1674.0 Safari/537.36"
}
session = requests.Session()
session.headers.update(headers)
