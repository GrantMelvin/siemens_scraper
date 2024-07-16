from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os
import re

# Target PDF folder
download_folder = 'C:/Users/grmelv/OneDrive - SAS/Desktop/siemens_scraper/data/pdfs'

# Keeps the browser open after we end the session and selects our chromedriver
options = Options()
options.add_experimental_option("detach", True)
service = Service("C:/Users/grmelv/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

# Attaches everything for the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Removes invalid characters from the filename
def sanitize_filename(filename):
    filename = filename.split('?')[0]            # Remove query parameters
    return re.sub(r'[\/:*?"<>|]', '', filename)  # Remove invalid characters

try:
    print(f'Downloading PDFs to: {download_folder}')

    # Where all of the URLs are stored
    main_url = f'https://support.industry.siemens.com/cs/products?ps=100&search=1LE10231DB222FA4&mfn=ps&o=DefaultRankingDesc&lc=en-US'
    driver.get(main_url)

    # Wait until the table is present
    wait = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table-header"))
    )

    #Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find all the <a> tags within the specified class
    links = soup.select("span[data-part='titlePart'] a")
    
    # Extract href attributes that match the pattern
    filtered_links = [link['href'] for link in links if 'document/' in link['href']]

    # The driver messes up sometimes and tries to click something that isnt there
    if(len(filtered_links)) == 0:
        print('Whoops. Restart!')

    # Base URL to attach the individual links
    base_url = 'https://support.industry.siemens.com/cs/'

    
    for url in filtered_links:
        # Link to evaluate in the list of items that we want to parse for PDFs
        full_url = base_url + url

        try:
            # Goes to the main page with the list of links we want to extract pdfs from
            driver.get(full_url)
            flag = False

            # Wait for the post content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[@data-bind='text: title, attr: { lang: selectedLanguage }'][@lang='en']"))
            )

            # Translates current page into HTML
            post_page_source = driver.page_source
            post_soup = BeautifulSoup(post_page_source, 'html.parser')

            # Find all PDF links
            # There are different notations they have PDFs under, therefore you need different identifiers
            pdf_links = post_soup.select('[data-bind="switch: pdfLink()"] a')
            pdf_links += post_soup.select('ul[data-part="pdfLinkPart"] li a')
            pdf_links += post_soup.select('li.category-block.download a')
            pdf_links += post_soup.select('a[data-file-download].attLnk')
            pdf_links += post_soup.select('a[data-bind*="pdfLink() + \'?download=true\'"]')

            # Loops through all the pdfs we find on the page
            for pdf_link in pdf_links:
                flag = True
                pdf_url = pdf_link['href']
                pdf_filename = sanitize_filename(os.path.basename(pdf_url))
                pdf_path = os.path.join(download_folder, pdf_filename)

                # Ensure the full URL is constructed correctly
                # If it doesnt have http - it will throw an error when you try to download
                if not pdf_url.startswith('http'):
                    pdf_url = base_url + pdf_url

                # Sends a request to download the pdf
                response = requests.get(pdf_url)
                with open(pdf_path, 'wb') as file:
                    file.write(response.content)

            if(flag):   # Debugging
                print(f"PDF found on {full_url}")
            else:       # Debugging
                print(f"No PDF found on {full_url}")

            # Go back to the main page so that we have access to the next page link
            driver.get(main_url)

        except Exception as e:
            print(f'ERROR:{e}')

except Exception as e:
    print(f"ERROR: {e}")
finally:
    driver.quit()
