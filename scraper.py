import csv
import requests
from bs4 import BeautifulSoup


class Scraper:
    # TODO comments
    # TODO Check if data is any unusale (twice the same fuel_type)

    def __init__(
        self,
        url = 'https://www.unitedconsumers.com/brandstofprijzen',
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'} ,
        filename = 'data.csv',
    ):
        self.url = url
        self.headers = headers
        self.filename = filename
        self.fuel_data = []
        self.field_names = ['name', 'price', 'difference']

    def run(self):
        # TODO check if elements are renamed
        soup = BeautifulSoup(self.__get_html(), 'html5lib')
        table_rows = soup.find_all('div', attrs = {'class':'row table-row'})

        for row in table_rows:
            fuel_type = self.__clean_text(row.find('a').text)
            fuel_info = row.find_all('div', attrs = {'class': 'col-xs-4 col-sm-4 text-right'})
            price = self.__clean_text(fuel_info[0].text)
            difference = self.__clean_text(fuel_info[1].text)

            # TODO maybe make it a list, dubble info
            self.fuel_data.append({'name': fuel_type, 'price': price, 'difference': difference})

    def __get_html(self):
        # TODO check if url is still alive
        r = requests.get(self.url)
        return r.content

    def save_to_csv(self):
        # TODO check if file is valid
        with open(self.filename, 'w', newline='') as f: 
            writer = csv.DictWriter(f, fieldnames = self.field_names) 
            writer.writeheader() 
            writer.writerows(self.fuel_data) 

    def __clean_text(self, text):
        cleaned_text = text.replace(' ', '')
        cleaned_text = cleaned_text.replace('\n', '')
        cleaned_text = cleaned_text.replace('€', '')
        cleaned_text = cleaned_text.replace(',', '.')

        try:
            cleaned_text = float(cleaned_text)
        except Exception as e:
            # TODO make better
            pass

        return cleaned_text


if __name__ == '__main__':
    scraper = Scraper()
    scraper.run()
    scraper.save_to_csv()
    print(scraper.fuel_data)