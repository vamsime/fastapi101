import time
import requests

def main():
    request_count = 100
    url = "https://httpbin.com/get"
    session = requests.Session()
    for idx in range(request_count):
        print(f"making request {idx + 1}")
        resp = session.get(url)
        if resp.status_code == 200:
            pass


start = time.time()
main()
end = time.time()
print(f"Time elapsed: {end-start}")