import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class url_scraper:
    def __init__(self, url,tag):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.data = []
        
    # Extract winner prizes from the HTML
    def extract_winner_numbers(self, main_prize_class = "col-12 text-center", other_prize_classes = "col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify"):
        main_prize_div = self.soup.find('div', class_=main_prize_class)
        if main_prize_div:
            main_prizes = main_prize_div.text.strip()
            main_prize_numbers = re.findall(r'PRIMER PREMIO(\d{5}) | SEGUNDO PREMIO (\d{5}) | TERCER PREMIO (\d{5})', main_prizes)
            self.data.append({
                'Prize type': 'Main Prize',
                'First Prize':main_prize_numbers[0][0],
                'Second Prize':main_prize_numbers[1][1],
                'Third Prize':main_prize_numbers[2][2],
            })
            
    