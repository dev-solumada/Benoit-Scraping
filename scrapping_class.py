import bs4


from bs4 import BeautifulSoup
from st_aggrid import AgGrid

import pandas 
import time
import streamlit
import requests

class Scrapping():

    def __init__(self, url):
        self.url = url

        self.status = { 'page_loaded': False, 'data_get': False, 'data_cleaned': False }

        self.page = self.load_html(self.url)

        self.soup = BeautifulSoup(self.page, 'lxml')
        if self.soup:
            pass
        else:
            time.sleep(9)

        self.taget_page = self.soup.find('div', class_='col-md-5 landing-page-table-container')
        self.rows = self.taget_page.find_all_next('div', class_='row')

        time.sleep(6)
        if self.rows:
            del(self.row[0])

        self.data_list = self.get_data(self.rows)

        self.flags, self.countries, self.patents, self.designs, self.trademarks = self.clean_data(self.data_list)

        while True:
            if self.status['data_cleaned'] != True: pass
            else: break

        if len(self.flags) == len(self.countries) and len(self.designs) == len(self.flags) and len(self.countries) == len(self.trademarks):
            self.dataFrame = pandas.DataFrame({"Flags":self.flags, "Countries":self.countries, "Patents":self.patents, "Designs":self.designs, "Trademarks":self.trademarks})
        else:
            self.dataFrame = None


    def load_html(self, url):
        """function to load page from url request"""
        response = requests.get(url)
        if not response.ok:
            print(f"{response.status_code}, url: {url}")
            self.status['page_loaded'] = True
        return response.text

    def get_data(self, datas):
        """function to get all data and return it as a list"""
        self.all_data = list()
        for i in range(len(datas)):
            self.flag = datas[i].find('img', class_='primary-border-color')['src']
            self.country = datas[i].find('div', class_='geo-grid-drawing-container col-md-2 countryBodyClass').text
            self.patent = datas[i].find('div', class_='geo-grid-data col-md-2 patentBodyClass').text
            try:
                self.design = datas[i].find('div', class_='geo-grid-data col-md-2 designBodyClass').find('div', class_='countButtonClass primary-btn-color').text
            except:
                self.design = datas[i].find('div', class_='geo-grid-data col-md-2 designBodyClass').find('div', class_='countButtonClass-zero').text
            try:
                self.trademark = datas[i].find('div', class_='geo-grid-data col-md-2 tmBodyClass').find('div', class_='countButtonClass primary-btn-color').text 
            except:
                self.trademark = datas[i].find('div', class_='geo-grid-data col-md-2 tmBodyClass').find('div', class_='countButtonClass-zero').text

            self.new_data = Data(flag=self.flag, country=self.country, design=self.design, patent=self.patent, trademark=self.trademark)
            self.all_data.append(self.new_data)
        
        self.status['data_get'] = True
        return self.all_data

    def clean_data(self, datas):
        """function to clean the data and return lists"""
        flags = list()
        countries = list()
        patents = list()
        designs = list()
        trademarks = list()

        for data in datas:
            flags.append(data.flag)
            countries.append(data.country)
            patents.append(data.patent)
            designs.append(data.design)
            trademarks.append(data.trademark)
        self.status['data_cleaned'] = True

        return flags, countries, patents, designs, trademarks

    def get_dataFrame(self):
        """function to return dataframe if everything is ok"""
        if self.status['page_loaded'] and self.status['data_get'] and self.status['data_cleaned']:
            print(f"Page not loaded...\nData not yet loaded\nData not cleaned yet")
            return
        else: return self.dataFrame


if __name__ == '__main__':

    url = "http://regionalip.aripo.org/wopublish-search/public/home?1"
    
    scrap = Scrapping(url)


    streamlit.set_page_config(page_title="WebScraping", layout="wide") 
    streamlit.title("""ARIPO Regional Homepage data""")
    launch_scrap = streamlit.button("Launch scrapping")
    donwloadFile = streamlit.button("Download file")

    def launch_scrapping():
        streamlit.write("getting the page")
