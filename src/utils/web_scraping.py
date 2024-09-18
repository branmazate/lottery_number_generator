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
        self.other_data = []
        self.main_data = []
        
    def scrape_data(self, url:str, tag:str, main_class:str, other_class:str = None, main_class_pattern:str=None, other_class_pattern:str=None):
        "Extracts de text from the given tag, main_class, and other_class based on a regular expression pattern."
        #TODO Add error handling for the case when the tag is not found.
        #TODO Add error handling for the case when the main_class is not found.
        #TODO Add error handling for the case when the other_class is not found.
        #TODO Add html content to the data obtained
        #FIXME All the entries in the main and other data are the same.
        try:
            #Extracting main class data.
            self.url = url
            self.response = requests.get(self.url)
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            tag_content = self.soup.find(tag, class_=main_class) #Gets the info from the main class
            if tag_content:
                main_class_text = tag_content.get_text().strip()
                print(f'Main class {tag} content: ',main_class_text)
                if main_class_pattern:
                    main_data = re.findall(main_class_pattern, main_class_text)
                    if main_data:
                        print(f'Extracted main data based on pattern: {main_data}')
                        self.main_data.append(main_data)
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
                            self.other_data.append(other_data)
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
    
    def turn_to_df(self, main_dict, other_dict=None,filepath = None):
        try:
            #Convert the data to a DataFrame
            for text in self.main_data:
                main_dict[0] = text[0]
                main_dict[1] = text[1]
                main_dict[2] = text[2]
            if other_dict:
                for text in self.other_data:
                    other_dict[0] = text[0]
                    other_dict[1] = text[1]
                    other_dict[2] = text[2]
            main_df = pd.DataFrame(main_dict)
            other_df = pd.DataFrame(other_dict)
            
            df = pd.concat([main_df, other_df], ignore_index=True)
            
            if filepath:
                df.to_csv(filepath, index=False)
                print(f'Data succesfully saved to {filepath}')
            else:
                print(f'Data succesfully saved')
                return df
            
        except Exception as e:
            print(f'Error saving data to CSV: {e}')