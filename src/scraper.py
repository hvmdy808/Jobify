from urllib.parse import quote_plus
import requests
from requests import Response
import time
from bs4 import BeautifulSoup
import math

class wuzzufScraper:
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

    def _safe_text(self, parent, tag, attrs=None, default=None):
        element = parent.find(tag, attrs or {})
        return element.get_text(strip=True) if element else default

    def _getData(self, card: BeautifulSoup):
        info: dict = {}

        info['job_title'] = self._safe_text(
            card, 'a', {'rel': 'noreferrer', 'class': 'css-o171kl'}
        )
        info['company'] = self._safe_text(
            card, 'a', {'class': 'css-ipsyv7'}
        )
        info['loc'] = self._safe_text(
            card, 'span', {'class': 'css-16x61xq'}
        )
        info['posting_recency'] = self._safe_text(
            card, 'div', {'class': ['css-eg55jf', 'css-1jldrig']}
        )
        info['employment_type'] = self._safe_text(
            card, 'span', {'class': 'css-uc9rga'}
        )
        info['work_arrangement_type'] = self._safe_text(
            card, 'span', {'class': 'css-uofntu'}
        )

        parent = card.find('div', {'class': 'css-1rhj4yg'})
        if parent:
            divs = parent.find_all("div", recursive=False)
            if len(divs) > 1:
                div = divs[1]
                info['experience_lvl'] = self._safe_text(div, 'a')
                info['years_of_experience'] = self._safe_text(div, 'span')

                a_list = div.find_all('a', recursive=False)

                skill_coll = [
                    a.get_text(strip=True)
                    for a in a_list[1:]
                ]
                info['skills'] = skill_coll

            else:
                info['experience_lvl'] = None
                info['years_of_experience'] = None
                info['skills'] = []

        else:
            info['experience_lvl'] = None
            info['years_of_experience'] = None
            info['skills'] = []

        return info


    def _normalize(self, denormalized_info: dict):
        normalized: list[dict] = []
        skills: list = denormalized_info['skills']
        for i in range(len(skills)):
            info: dict = {}
            info['job_title'] = denormalized_info['job_title']
            info['company'] = denormalized_info['company']
            info['loc'] = denormalized_info['loc']
            info['posting_recency'] = denormalized_info['posting_recency']
            info['employment_type'] = denormalized_info['employment_type']
            info['work_arrangement_type'] = denormalized_info['work_arrangement_type']
            info['experience_lvl'] = denormalized_info['experience_lvl']
            info['years_of_experience'] = denormalized_info['years_of_experience']
            info['skill'] = skills[i]
            normalized.append(info)

        return normalized


    def scrape(self, titles: list[str], base_url: str):
        final: list[dict] = []
        pages: list[Response] = []
        for i in range(len(titles)):
            pages.clear()
            pages.append(self._sendRequest(base_url= base_url, title= titles[i], page_no= 1))
            jobs_no = self._getNoOfJobs(response= pages[0])
            #print(f'Number of found job: {jobs_no}')
            remaining_pages = math.ceil(jobs_no / 15) - 1
            # remaining_pages = 3
            #print(f'Pages: {remaining_pages+1}')
            for j in range(remaining_pages):
                pages.append(self._sendRequest(base_url=base_url, title=titles[i], page_no= j + 2))

            for k in range(len(pages)):
                soup = BeautifulSoup(pages[k].content, 'html.parser')
                cards = soup.find_all('div', {'class':'css-ghe2tq'})
                for l in range(len(cards)):
                    #print(f'Current page: {k + 1}, Current card: {l + 1}')
                    denormalized: dict = self._getData(card= cards[l])
                    normalized: list[dict] = self._normalize(denormalized)
                    final.extend(normalized)


        return final
