from bs4 import BeautifulSoup
import streamlit
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

import time 
import pandas
import requests

class Data():

    def __init__(self, flag, country, patent, design, trademark):

        self.flag = flag
        self.country = country
        self.patent = patent
        self.design = design
        self.trademark = trademark

    def describe(self):
        print(f"flag : {self.flag} \tcountry : {self.country} \tpatent : {self.patent}\tdesign : {self.design} \ttrademark : {self.trademark}\n")


def load_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f"{response.status_code}, url: {url}")
    return response.text

url = "http://regionalip.aripo.org/wopublish-search/public/home?1"

pages = load_html(url)

soup = BeautifulSoup(pages, 'lxml')
target_page = soup.find('div', class_='col-md-5 landing-page-table-container')
rows = target_page.find_all_next('div', class_='row')

del(rows[0])

flags, countries, patents, designs, trademarks = list(), list(), list(), list(), list()

all_datas = list()


for i in range(len(rows)):
    flag = rows[i].find('img', class_='primary-border-color')['src']
    country = rows[i].find('div', class_='geo-grid-drawing-container col-md-2 countryBodyClass').text
    patent = rows[i].find('div', class_='geo-grid-data col-md-2 patentBodyClass').text
    try:
        design = rows[i].find('div', class_='geo-grid-data col-md-2 designBodyClass').find('div', class_='countButtonClass primary-btn-color').text
    except:
        design = rows[i].find('div', class_='geo-grid-data col-md-2 designBodyClass').find('div', class_='countButtonClass-zero').text
    try:
        trademark = rows[i].find('div', class_='geo-grid-data col-md-2 tmBodyClass').find('div', class_='countButtonClass primary-btn-color').text 
    except:
        rows[i].find('div', class_='geo-grid-data col-md-2 tmBodyClass').find('div', class_='countButtonClass-zero').text
    
    new_data = Data(flag=flag, country=country, design=design, patent=patent, trademark=trademark)
    all_datas.append(new_data)

for data in all_datas:
    flags.append(data.flag)
    countries.append(data.country)
    patents.append(data.patent)
    designs.append(data.design)
    trademarks.append(data.trademark)

table = pandas.DataFrame({"Flags": flags, "Countries": countries, "Patents": patents, "Designs": designs, "Trademarks":trademarks})
streamlit.set_page_config(page_title="WebScraping", layout="centered") 
streamlit.title("""ARIPO Regional Homepage data""")

text = streamlit.write("")
col1, col2 = streamlit.columns(2)


gd = GridOptionsBuilder.from_dataframe(table)
gd.configure_pagination(enabled=True)
gridoptions = gd.build()


with col1:
    launch_scrap = streamlit.button("Launch scrapping")
    download = streamlit.button("Download file")



with col2:
    pass

if launch_scrap:
    AgGrid(table, gridOptions=gridoptions, allow_unsafe_jscode=True, theme='material')
    time.sleep(.9)
    # if datagrid: streamlit.info(len(table))




if download:
    table.to_xml("aripo_data.x")

    


    
