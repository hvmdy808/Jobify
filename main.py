import requests
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from src.scraper import wuzzufScraper
from src.config import Titles
from src.config import urls
from src.CSVLS import CSV


def main():
    scraper = wuzzufScraper()
    result = scraper.scrape(titles= Titles, base_url= urls[0])
    # for row in result:
    #     print(row)

    print((len(result)))

    csv = CSV()
    csv.save(data= result, filename= 'initial')




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