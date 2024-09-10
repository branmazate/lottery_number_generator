import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class url_scraper:
    def __init__(self):
        """
        Initializes the URLScraper class.
        
        Parameters:
        url (str): The URL to scrape.
        """
        self.url = ''
        self.main_html_content = ""
        self.secondary_html_content = ""
        self.data = []
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        
    def scrape_data(self, url:str, tag:str, main_class:str, other_class:str = None, main_class_pattern:str=None, other_class_pattern:str=None):
        "Extracts de text from the given tag, main_class, and other_class based on a regular expression pattern."
        try:
            #Extracting main class data.
            self.url = url
            tag_content = self.soup.find(tag, class_=main_class) #Gets the info from the main class
            if tag_content:
                main_class_text = tag_content.get_text().strip()
                print(f'Main class {tag} content: ',main_class_text)
                if main_class_pattern:
                    main_data = re.findall(main_class_pattern, main_class_text)
                    if main_data:
                        print(f'Extracted main data based on pattern: {main_data}')
                    else:
                        print(f'No main data found based on pattern: {main_class_pattern}')
            #Extracting other class data.
            if other_class:
                other_class_content = self.soup.find(tag, class_=other_class)
                if other_class_content:
                    other_class_text = other_class_content.get_text().strip()
                    print(f'Other class {tag} content: ',other_class_text)
                    if other_class_pattern:
                        other_data = re.findall(other_class_pattern, other_class_text)
                        if other_data:
                            print(f'Extracted other data based on pattern: {other_data}')
                        else:
                            print(f'No other data found based on pattern: {other_class_pattern}')
            else:
                print(f'No other class provided')
                    
        except Exception as e:
            print(f'Error in extracting data {e}')
                
        
    # # Extract winner prizes from the HTML
    # def extract_winner_numbers(self, start_id, end_id):
    #     for id in range(start_id, end_id+1):
    #         url = f'{self.url}?id={id}'
    #         response = requests.get(url)
    #         if response.status_code ==200:
    #             html_content =  response.text #Gets raw HTML content
    #             print(f'HTML content succesfully extracted')
    #         else:
    #             raise Exception('Failed to retrieve the page. Status code: {response.status_code}')
    #         main_prizes, other_prizes = self.scrape_data(main_prize_class = "col-12 text-center", other_prize_classes = "col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify")
            
    #         if main_prizes and other_prizes:
    #             self.data.append(
    #                 {'url':url,
    #                  'main_prizes':main_prizes,
    #                  'other_prizes':other_prizes})
    #         else:
    #             print(f'No data available for id: {id}')
                
    # def save_to_csv(self, filepath='scraped_data.csv'):
    #     """
    #     Saves the scraped data to a csv file
        
    #     Parameters:
    #     filename(str): The name of the CSV file to save the data
    #     """
        
    #     try:
    #         #Convert the data to a DataFrame
    #         df = pd.DataFrame(self.data)
    #         #Save DataFrame to a CSV ile
    #         df.to_csv(filepath, index=False)
    #         print(f'Data succesfully saved to {filepath}')
    #     except Exception as e:
    #         print(f'Error saving data to CSV: {e}')