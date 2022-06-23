from bs4 import BeautifulSoup

import pandas as pd 
import requests
import time
import streamlit
import numpy



def load_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f"{response.status_code}, url: {url}")
    return response.text


url = "http://regionalip.aripo.org/wopublish-search/public/patents?2&query=OFCO:GM"


html_page = load_html(url)
soup = BeautifulSoup(html_page, 'lxml')

documents, titles, statuses, originals, filing_dates, pub_numbers, pub_dates, priority_details, ipc_classes, org_reg_numbs, reg_dates, applicants, inventors, des_states = list()


class Document():
    
    def __init__(self, status, title, original, filing_date, publication_number, publication_date, priority_Detail, ipc_class, org_reg_numb, reg_date, applicant, inventor, designated_states):
        self.status = status
        self.title = title 
        self.original = original
        self.filing_date = filing_date
        self.publication_number = publication_number
        self.publication_date = publication_date
        self.priority_Detail = priority_Detail
        self.ipc_class = ipc_class
        self.org_reg_numb = org_reg_numb
        self.reg_date = reg_date
        self.applicant = applicant
        self.inventor = inventor
        self.designated_states = designated_states

    def describe(self):
        print(
            f"\
            status: {self.status}\n\
            title: {self.title}\n\
            Original filing Number: {self.original}\n\
            Filing date: {self.filling_date}\n\
            Publication Number: {self.publication_number}\n\
            Publication Date: {self.publication_date}\n\
            Priority details: {self.priority_Detail}\n\
            IPC Classes: {self.ipc_class}\n\
            Origin registration Number: {self.org_reg_numb}\n\
            Registration Date: {self.reg_date}\n\
            Applicant: {self.applicant}\n\
            Inventor: {self.inventor}\n\
            Designated States: {self.desiganted_states}"
        )

print(f"titles: {titles} originals: {originals}")