import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
base_url = "https://www.media.volvocars.com/global/en-gb/Corporate/sales-volumes?year={year}&month={month}"

# Years and months to scrape
years = list(range(2018, 2024))
months = list(range(1, 13))

# List to store scraped data
data = []

# Loop through each year and month
for year in years:
    for month in months:
        url = base_url.format(year=year, month=month)
        print(f"Fetching data for {year}-{month:02d} from {url}")
        
        # Fetch the HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the sales table
        table = soup.find('table', class_='table table-striped')
        
        if table:
            # Extract table headers
            headers = [header.text.strip() for header in table.find_all('td', class_='header')]
            
            # Extract table rows
            rows = table.find_all('tr')[1:]  # Skip the header row
            
            for row in rows:
                if row.find('td', class_='footer'):
                    # Skip the total row
                    continue
                columns = row.find_all('td')
                model_data = [col.text.strip() for col in columns]
                
                # Append year and month to the data
                model_data.insert(0, year)
                model_data.insert(1, month)
                
                # Add the row data to the list
                data.append(model_data)
                


# Create a pandas DataFrame
columns = ['Year', 'Month'] + headers
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to a CSV file
df.to_csv(f'volvo_sales_data.csv', index=False)

print(f"Data scraping completed and saved to volvo_sales_data.csv")
