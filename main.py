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
    print('Hi')
    print(formatString('Hamdy Mohamed'))




if __name__ == '__main__':
    main()
