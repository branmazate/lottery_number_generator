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
        
    def scrape_data(self, url:str, tag:str, main_class:str, data:dict, other_class:str = None, main_class_pattern:str=None, other_class_pattern:str=None):
        "Extracts de text from the given tag, main_class, and other_class based on a regular expression pattern."
        #TODO Add error handling for the case when the tag is not found.
        #TODO Add error handling for the case when the main_class is not found.
        #TODO Add error handling for the case when the other_class is not found.
        #TODO Add html content to the data obtained
        try:
            #Extracting main class data.
            self.url = url
            self.response = requests.get(self.url)
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            self.data = data
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
            
    def scrape_data_from_range(self, url:str, url_pattern:str, start:int,end:int,tag:str,main_class:str, other_class:str = None, main_class_pattern:str=None, other_class_pattern:str=None):
        #TODO Add error handling for the case when it finds no elements or invalid elements from some values on the range.
        for id in range(start, end+1):
            url = f'{url}{url_pattern}{id}'
            self.scrape_data(url,tag=tag,main_class=main_class,other_class=other_class,main_class_pattern=main_class_pattern,other_class_pattern=other_class_pattern)
    
      
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