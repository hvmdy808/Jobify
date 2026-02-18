from src.scraper import wuzzufScraper
from src.config import Titles
from src.config import urls
from src.CSVLS import CSV
from src.WuzzufCleaner import WuzzufCleaner
import pandas as pd


def main():
    scraper = wuzzufScraper()
    result = scraper.scrape(titles= Titles, base_url= urls[0])

    print((len(result)))

    csv = CSV()
    csv.save(data= result, filename= 'initial')

    cleaner = WuzzufCleaner()
    cleaner.clean(data= 'initial', filename= 'cleaned')

    df = pd.read_csv(f'D:\\Projects\\PycharmProjects\\Jobify\\data\\cleaned.csv')
    df.info()



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