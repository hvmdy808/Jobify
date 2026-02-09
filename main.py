import requests
from bs4 import BeautifulSoup


def formatString(string: str):
    modified = string.lower().strip()
    modified = modified.replace(' ', '+')
    return modified

def formURL(job_tilte: str, location: str, page_no: int):
    start = (page_no - 1) * 10
    url = f'https://eg.indeed.com/jobs?q={formatString(job_tilte)}&l={formatString(location)}&radius=25&from=searchOnDesktopSerp'

    if page_no > 1:
        url += f'start={start}'

    return url


def main():
    url = formURL('Data analyst', 'remote', 0)
    print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    proxies = {
        "http": "http://123.123.123.123:8080",
        "https": "http://123.123.123.123:8080"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            print("Access forbidden. The website is blocking automated requests.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Some other request error occurred: {req_err}")
    else:
        print("Request successful!")
        print(response.status_code)







if __name__ == '__main__':
    main()
