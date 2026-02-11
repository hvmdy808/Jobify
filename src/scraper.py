from urllib.parse import quote_plus
import requests
import time
from bs4 import BeautifulSoup
import math

class wazzufScraper:
    def _formatString(self, string: str):
        return quote_plus(string.strip())

    def _formURL(self, base_url: str, job_title: str, page_no: int):
        start = max(0, page_no - 1)

        url = f'{base_url}{self._formatString(job_title)}'

        if page_no > 1:
            url += f'&start={start}'

        return url


    def _sendRequest(self, base_url: str, title: str, page_no: int):
        session = requests.Session()

        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        })

        url = self._formURL(base_url= base_url, job_title= title, page_no= page_no)

        try:
            time.sleep(2)
            response = session.get(url, timeout=15)
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
            return response
            # print(response.text)

    def _getNoOfJobs(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').contents[0]
        num = ''
        title_text = title.text
        for i in range(len(title_text)):
            if title_text[i] == ' ':
                break
            if title_text[i] == ',':
                pass
            else:
                num += title_text[i]

        return int(num)

    def getData(self, titles: list[str], url: str):
        for i in range(len(titles)):
            res = self._sendRequest(base_url= url, title= titles[i], page_no= 1)
            jobs_no = self._getNoOfJobs(response= res)
            remaining_pages = math.ceil(jobs_no / 15) - 1
            for j in range(remaining_pages):
                res = self._sendRequest(base_url=url, title=titles[i], page_no= j + 2)

