import requests
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


def formatString(string: str):
    return quote_plus(string.lower().strip())

def formURL(job_tilte: str, location: str, page_no: int):
    start = max(0, (page_no - 1) * 10)
    url = f'https://eg.indeed.com/jobs?q={formatString(job_tilte)}&l={formatString(location)}&radius=25&from=searchOnDesktopSerp'

    if page_no > 1:
        url += f'&start={start}'

    return url


def main():
    url = "https://wuzzuf.net/search/jobs/?q=data"
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    })

    try:
        time.sleep(2)
        response = session.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            print("Access forbidden. The website is blocking automated requests.")
        else:
            print(f"HTTP error occurred: {http_err}")
    else:
        print("Request successful!")
        print(response.status_code)
        print(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').contents[0]
        print(title)
        num = ''
        title_text = title.text
        for i in range(len(title_text)):
            if title_text[i] == ' ':
                break
            if title_text[i] == ',':
                pass
            else:
                num += title_text[i]

        print(int(num) - 1)


        cards = soup.find_all('div', {'class':'css-ghe2tq'})
        print(cards)
        print(len(cards))






if __name__ == '__main__':
    main()







'''
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Some other request error occurred: {req_err}")
'''