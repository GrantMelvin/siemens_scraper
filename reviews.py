from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import os

current_directory = os.getcwd()

# Keeps the browser open after we end the session and selects our chromedriver
options = Options()
options.add_experimental_option("detach", True)
service = Service("C:/Users/grmelv/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

# Attaches everything for the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Pick up from where you left off last time
START = 319
counter = START

try:
    main_url = f'https://support.industry.siemens.com/forum/WW/en/topics/#!?&SortOrder=lastpost_desc&PageNumber={counter}&PageSize=50'
    driver.get(main_url)

    def extract_posts():
        # Wait until the table is present
        wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "std-table"))
        )
        #Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        #print(soup)
        
        # Find all the <a> tags within the specified class
        links = soup.select('div.std-table tbody a')
        # print(links)

        # Extract href attributes that start with /forum/WW/en/posts/
        forum_links = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('/forum/WW/en/posts/')]
        # print(forum_links)

        base_url = 'https://support.industry.siemens.com'
        for url in forum_links:
            full_url = base_url + url
            print(f"Current: {url.strip('?page=0&pageSize=10')}")

            try:

                # Navigate to the individual post page
                driver.get(full_url)

                # Wait for the post content to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'post-list'))
                )
                
                post_page_source = driver.page_source
                post_soup = BeautifulSoup(post_page_source, 'html.parser')

                # Extract user, content, and date from the post page
                for post in post_soup.select('table', {'class':'dns'}):
                    date = post.find('a', {'name': True}).text.strip()
                    user = post.find('a', {'data-targetdialog': 'profile'}).text.strip()
                    content = post.find('span', {'class': 'scrollOnMaxWidth'}).text.strip()

                    entry = {
                        "thread":full_url,
                        "user":user,
                        "date":date,
                        "content":content
                    }
                    # print(entry)

                    # Open and read the existing JSON file
                    with open('./data/forumData.json', 'r') as openfile:
                        json_array = json.load(openfile)

                    # Append the new entry to the list
                    json_array.append(entry)

                    # Write the updated list back to the JSON file
                    with open('./data/forumData.json', 'w') as openfile:
                        json.dump(json_array, openfile, indent=4)

            except Exception as e:
                continue
            
    extract_posts()
    # Navigate through pagination
    while True:
        driver.get(f'https://support.industry.siemens.com/forum/WW/en/topics/#!?&SortOrder=lastpost_desc&PageNumber={counter}&PageSize=50')
        counter += 1
        print(f"CURRENTLY ON PAGE: {counter}")
        try:
            # Check if 'Next' button exists and click it
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagination.next[ng-click*="setPage"]'))
            )
            next_button.click()

            wait = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "std-table"))
            )
            
            # Extract posts from the new page
            extract_posts()
        
        except Exception as e:
            print("No more pages or error occurred:", e)

            missed = {'error': counter}

            # Open and read the existing JSON file
            with open('./data/forumMissed.json', 'r') as openfile:
                json_array = json.load(openfile)

            # Append the new entry to the list
            json_array.append(missed)

            # Write the updated list back to the JSON file
            with open('./data/forumMissed.json', 'w') as openfile:
                json.dump(json_array, openfile, indent=4)
            continue


except Exception as e:
    print(f"ERROR: {e}")
finally:
    driver.quit()
