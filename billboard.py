import json
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class Billboard:
    def __init__(self, date: str = '2023-04-08'):
        self.date = date
        self.endpoint = f'https://www.billboard.com/charts/hot-100/{self.date}'
        logging.debug('Billboard class created')

    def get_list(self) -> list | None:
        response = requests.get(self.endpoint)
        logging.debug(f'The status code for the request was {response.status_code}')
        soup = BeautifulSoup(response.text, features="html.parser")
        top_100_table = soup.find(class_='chart-results-list')
        if top_100_table:
            logging.debug('Top 100 list found')
            table = BeautifulSoup(str(top_100_table), features="html.parser")
            table_rows = table.find_all(class_="o-chart-results-list-row-container")
            if table_rows:
                logging.debug(f'Top 100 table contains {len(table_rows)} entries')
                cleaned_song_titles = []
                for song_entry in table_rows:
                    song_title = BeautifulSoup(str(song_entry), features="html.parser").find(id='title-of-a-story').text
                    if song_title:
                        name = "".join(item for item in song_title if item.isprintable())
                        logging.debug(f'Song titled - {name} found')
                        cleaned_song_titles.append(name)
                    else:
                        logging.debug('No title found')
                logging.debug('Song title list has been returned')
                return cleaned_song_titles
            else:
                logging.debug('No table entry found')
                logging.debug('Song title list has been returned')
                return None
        else:
            logging.debug('Top 100 list not found')
            logging.debug('Song title list has been returned')
            return None


if __name__ == '__main__':
    today = datetime.now()
    date = today.strftime('%Y-%m-%d')
    bill = Billboard(date=date)
    name = bill.get_list()
    with open('name_list.json', mode='w') as json_file:
        lists = {'Song title': name}
        json.dump(lists, json_file, indent=4)
