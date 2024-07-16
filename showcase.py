from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Keeps the browser open after we end the session and selects our chromedriver
options = Options()
options.add_experimental_option("detach", True)
service = Service("C:/Users/grmelv/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

# Attaches everything for the webdriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to the main page
    main_url = 'https://support.industry.siemens.com/cs/products?dtp=TechnicalData&mfn=ps&lc=en-WW'
    driver.get(main_url)

    # Wait for the document headers to be present
    wait = WebDriverWait(driver, 10)
    document_headers = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="documentheader"]/parent::a')))

    # Get the document links
    document_links = [header.get_attribute('href') for header in document_headers]
    print(document_links)

    # Loop through each document link
    for document_link in document_links:
        print(f"Current link being evaluated: {document_link}")

        try:
            # Click on the individual product page
            driver.get(document_link)

            # Wait for table to load if it exists
            try:

                # Select the table
                table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))

                # Get the table content
                table_html = table.get_attribute('outerHTML')

                # Parse the content - can be JSON instead or go store somewhere
                soup = BeautifulSoup(table_html, 'html.parser')

                # Print the table content
                print(soup.prettify())

            # No table on this page
            except:
                print(f"No table found on: {document_link}")

            # Go back to main page so that we can go to the next product
            driver.get(main_url)

            # Wait for the main page to load again
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="documentheader"]/parent::a')))
        except Exception as e:
            print(f"ERROR ON {document_link}: {e}")

# Something has gone terribly wrong
except Exception as e:
    print(f"ERROR: {e}")