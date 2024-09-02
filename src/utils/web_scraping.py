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
        self.response = requests.get(url)
        if self.response.status_code == 200:
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            self.data = []
        else:
            raise Exception('Failed to retrieve the page. Status code: {self.response.status_code}')
        
    # Extract winner prizes from the HTML
    def extract_winner_numbers(self, main_prize_class = "col-12 text-center", other_prize_classes = "col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify"):
        """Extracts winner numbers and prize details from the HTML content

        Args:
            main_prize_class (str): The class name of the div containing the main prizes. Defaults to "col-12 text-center".
            other_prize_classes (str): The class name of the containing other prizes. Defaults to "col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify".
        """
        try:
            #Extract main prizes
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
            #Extract other prizes from the HTML.
            other_prize_divs = self.soup.find_all('div',class_=other_prize_classes)
            for div in other_prize_divs:
                winners_text = div.text.strip()
                winner_numbers = re.findall(r'(\d{5})',winners_text)
                prize_type = re.findall(r'(\d{5}\w+)')
                prize_amounts = re.findall(r'(\d+,\d+.\d+)',winners_text)

                for i in range(len(winner_numbers)):
                    self.data.append({
                        'Winner number': winner_numbers[i],
                        'Prize type': prize_type[i][5:],
                        'Prize amount': prize_amounts[i],
                    })
        except Exception as e:
            print(f"Error extracting winner numbers: {e}")
            
    def to_dataframe(self):
        """
        Converts the scraped data into a pandas Dataframe
        
        Returns:
        pd.DataFrame: The data as a pandas DataFrame
        """
        if self.data:
            df = pd.DataFrame(self.data)
            return df
        else:
            print("No data available.")
            return None
            
def generate_urls(base_url, start_id, end_id):
    """
    Generates a list of urls to scrape by changing the ID
    
    Parameters:
    base_url (str): The base URL
    start_id (int): The starting ID number
    end_id (int): The ending ID number
    
    Returns:
    list: A list of URLs
    """
    
    return [f'{base_url}?id={i}' for i in range (start_id,end_id+1)]

def scrape_multiple_pages(base_url,start_id,end_id,main_prize_class="col-12 text-center",other_prizes_class="col-xs-12 col-sm-12 col-md-4 col-lg-4 text-justify"):
    """
    Scrapes data from multiple pages by generating URLs in a loop.

    Parameters:
    base_url (str): The base URL.
    start_id (int): The starting ID number.
    end_id (int): The ending ID number.
    main_prize_class (str): The class name for the main prizes div.
    other_prizes_class (str): The class name for the other prizes div.

    Returns:
    pd.DataFrame: A DataFrame containing the scraped data.
    """
    all_data = pd.DataFrame()
    
    #generate URLs
    urls = generate_urls(base_url,start_id,end_id)
    
    #Loop through URLs and scrape data
    for url in urls:
        scraper = url_scraper(url)
        scraper.extract_winner_numbers(main_prize_class=main_prize_class, other_prize_classes=other_prizes_class)
        df = scraper.to_dataframe()
        all_data = pd.concat([all_data, df], ignore_index=True)
        
    return all_data