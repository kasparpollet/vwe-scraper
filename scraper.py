import sys
import csv
import requests
from bs4 import BeautifulSoup

save_to_file = False
get_data = False


class Scraper:
    # TODO comments
    # TODO Check if data is any unusale (twice the same fuel_type)

    def __init__(
        self,
        url = 'https://www.unitedconsumers.com/brandstofprijzen',
        filename = 'data',
    ):
        self.url = url
        self.filename = filename
        self.fuel_data = []
        self.field_names = ['name', 'price', 'difference']

    def run(self) -> None:
        with open(f'{self.filename}.html', 'r', newline='') as f:
            soup = BeautifulSoup(f.read(), 'html5lib')

        table_rows = soup.find_all('div', attrs = {'class':'row table-row'})

        if not table_rows:
            raise SystemExit('HTML elements can not be find, check if the website is updated')

        for row in table_rows:
            fuel_type = self.__clean_text(row.find('a').text)
            fuel_info = row.find_all('div', attrs = {'class': 'col-xs-4 col-sm-4 text-right'})
            price = self.__clean_text(fuel_info[0].text)
            difference = self.__clean_text(fuel_info[1].text)

            self.fuel_data.append({'name': fuel_type, 'price': price, 'difference': difference})

    def get_html(self) -> bytes:
        try:
            r = requests.get(self.url)
            r.raise_for_status()

            with open(f'{self.filename}.html', 'w', newline='') as f:
                f.write(r.text)
            return r.content

        except requests.exceptions.HTTPError as e:
            raise SystemExit(e) # Example bad request
            
        except requests.exceptions.ConnectionError as e:
            raise SystemExit(e) # Example no internet

    def save_to_csv(self) -> None:
        # TODO check if file is valid
        # TODO Add date to file name or row
        with open(f'P{self.filename}.csv', 'w', newline='') as f: 
            writer = csv.DictWriter(f, fieldnames = self.field_names) 
            writer.writeheader() 
            writer.writerows(self.fuel_data) 

    def __clean_text(self, text: str) -> str | float:
        cleaned_text = text.replace(' ', '')
        cleaned_text = cleaned_text.replace('\n', '')
        cleaned_text = cleaned_text.replace('€', '')
        cleaned_text = cleaned_text.replace(',', '.')

        try:
            cleaned_text = float(cleaned_text)
        except (TypeError, ValueError):
            pass # The string should stay a string

        return cleaned_text

def get_params() -> None:
    # TODO add arg for file path
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        if symbol == '-s':
            save_to_file = True
        if symbol == '-g':
            get_data = True

    elif len(sys.argv) > 2:
        symbol = sys.argv[2]
        if symbol == '-s':
            save_to_file = True
        if symbol == '-g':
            get_data = True


def scrape() -> dict:
    scraper = Scraper()

    if get_data:
        scraper.get_html()

    scraper.run()

    if save_to_file:
        scraper.save_to_csv()

    return scraper.fuel_data


if __name__ == '__main__':
    get_params()

    data = scrape()
    print(data)
