from bs4 import BeautifulSoup
import requests
import xlsxwriter
from datetime import datetime

# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Base URL with query parameters
base_url = 'https://www.property24.com/farms-for-sale/limpopo/14'
query_params = 'sp=se%3dTrue'

# Create a new Excel workbook with timestamp in the file name
workbook = xlsxwriter.Workbook(f"PropertyListings_{timestamp}.xlsx")
worksheet = workbook.add_worksheet("Property Listings")

# Add header row
worksheet.write(0, 0, "Price")
worksheet.write(0, 1, "Type of Property")
worksheet.write(0, 2, "Location")
worksheet.write(0, 3, "Bedrooms")
worksheet.write(0, 4, "Bathrooms")
worksheet.write(0, 5, "URL")

# Initialize row index
row_index = 1

# Iterate over each page
for page_number in range(1, 13):  # Total pages: 12
    # Construct URL for the current page
    if page_number == 1:
        url = f'{base_url}{query_params}'
    else:
        url = f'{base_url}/p{page_number}{query_params}'
    
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> elements representing individual listings
    listings = soup.find_all('a', title=lambda title: title and "Bedroom" in title)
    
    # Loop through each listing on the current page
    for listing in listings:
        # Extracting price, type, and location
        offers_span = listing.find('span', itemprop='offers')
        price = offers_span.find('span', class_='p24_price').text.strip() if offers_span else 'N/A'
        property_type = offers_span.find('span', class_='p24_title').text if offers_span else 'N/A'
        location = offers_span.find('span', class_='p24_location').text if offers_span else 'N/A'

        # Extracting bedrooms and bathrooms
        icons_span = listing.find('span', class_='p24_icons')
        bedrooms_span = icons_span.find('span', title='Bedrooms') if icons_span else None
        bathrooms_span = icons_span.find('span', title='Bathrooms') if icons_span else None

        bedrooms = bedrooms_span.find('span').text if bedrooms_span else 'N/A'
        bathrooms = bathrooms_span.find('span').text if bathrooms_span else 'N/A'

        # Extracting URL
        url = 'https://www.property24.com' + listing.get('href')

        # Write the extracted information to the worksheet
        worksheet.write(row_index, 0, price)
        worksheet.write(row_index, 1, property_type)
        worksheet.write(row_index, 2, location)
        worksheet.write(row_index, 3, bedrooms)
        worksheet.write(row_index, 4, bathrooms)
        worksheet.write(row_index, 5, url)

        # Increment row index
        row_index += 1

# Save the workbook
workbook.close()

print(f"Data saved to PropertyListings_{timestamp}.xlsx")
