import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class url_scraper:
    def __init__(self, url):
        """
        Initializes the URLScraper class.
        
        Parameters:
        url (str): The URL to scrape.
        """
        self.url = url
        self.data = []
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
    
    def scrape_data(self, main_prize_class = "col-12 text-center", other_prize_classes = "col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify"):
        try:
            #Extracting main prizes
            main_prize_div = self.soup.find("div", {"class": main_prize_class})
            if main_prize_div:
                main_prizes_text = main_prize_div.get_text(separator='|').strip()
                print("Main Prize Div Content:",main_prizes_text)
                main_prizes_pattern = r'PRIMER PREMIO(\d{5}) \|\|\| SEGUNDO PREMIO (\d{5}) \|\|\| TERCER PREMIO (\d{5})'
                main_prizes_match = re.findall(main_prizes_pattern, main_prizes_text)
                
                if main_prizes_match:
                    main_prizes = main_prizes_match[0]
                    print(f'Main Prizes: {main_prizes}')
                else:
                    print('Not enough main prizes found.')
                    main_prizes = None
            else:
                print('Main prize div not found.')
            #Extracting other prizes
            other_prizes_div = self.soup.find('div',class_=other_prize_classes)
            if other_prizes_div:
                other_prizes_text = other_prizes_div.get_text(' ').strip()
                print(f"Other prize div content: {other_prizes_text}")
                
                #Regular expression to extract the prizes
                other_prizes_pattern = r'(\d{5})\s+([A-Z]{1,3})\s+\.{4}\s+([\d.,]+)'
                other_prizes = re.findall(other_prizes_pattern, other_prizes_text)
                print(f'Other Prizes: {other_prizes}')
            else:
                print('Other prize div not found.')
                other_prizes = None
            return main_prizes, other_prizes
        except Exception as e:
            print(f'Error in extracting data: {e}')
        
    # Extract winner prizes from the HTML
    def extract_winner_numbers(self, start_id, end_id, main_prizes, other_prizes):
        for id in range(start_id, end_id+1):
            url = f'{self.url}?id={id}'
            response = requests.get(url)
            if response.status_code ==200:
                html_content =  response.text #Gets raw HTML content
                print(f'HTML content succesfully extracted')
            else:
                raise Exception('Failed to retrieve the page. Status code: {response.status_code}')
            main_prizes, other_prizes = self.scrape_data(main_prize_class = "col-12 text-center", other_prize_classes = "col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify")
            
            if main_prizes and other_prizes:
                self.data.append(
                    {'url':url,
                     'main_prizes':main_prizes,
                     'other_prizes':other_prizes})
            else:
                print(f'No data available for id: {id}')
                
    def save_to_csv(self, filepath='scraped_data.csv'):
        """
        Saves the scraped data to a csv file
        
        Parameters:
        filename(str): The name of the CSV file to save the data
        """
        
        try:
            #Convert the data to a DataFrame
            df = pd.DataFrame(self.data)
            #Save DataFrame to a CSV ile
            df.to_csv(filepath, index=False)
            print(f'Data succesfully saved to {filepath}')
        except Exception as e:
            print(f'Error saving data to CSV: {e}')