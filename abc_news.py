from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time


# Set up Chrome options to run headless (without opening a browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")
# Using a raw string by adding 'r' before the string or replacing backslashes with forward slashes
driver_path = r"C:\WebScraping( For NewsAlert)\chromedriver-win64\chromedriver.exe"
# Set up Chrome service
chrome_service = Service(driver_path)
# Create a new WebDriver instance for the main page
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


# List to store data
data = []

for i in range(1, 4):
    url = f"https://abcnews.go.com/search?searchtext=Bangladesh&page={i}"
    # Visit the URL with Selenium to allow JavaScript to execute
    driver.get(url)
    time.sleep(3)  # Adjust as needed to wait for dynamic content to load
    # Get the page source after it has fully loaded
    page_source = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    list_of_articles = soup.find('section', class_="ContentRoll")
    articles = soup.find_all('section', class_="ContentRoll__Item")
    # published_time_element = soup.find('div', class_='TimeStamp__Date ContentRoll__Date--recent')
    # if published_time_element:
    #     published_time = published_time_element.text.strip()
    #     print(f'Published Time: {published_time}')
    # else:
    #     print('Published time not found on the page.')
    #     published_time = "Not available"

    for article in articles:
        article_link = article.find('a')['href'].strip()

        # Visit the article link with the existing WebDriver instance
        driver.get(article_link)
        time.sleep(3)
        # Get the page source after the article page has fully loaded
        article_page_source = driver.page_source

        article_soup = BeautifulSoup(article_page_source, 'html.parser')

        # Extract the title, paragraph, and date from the article page
        title_element = article_soup.find('h2', class_="video-info-module__text--title")
        paragraph_element = article_soup.find('h3', class_="video-info-module__text--subtitle__vod")
        date_element = article_soup.find('h3', class_="video-info-module__text--subtitle__timestamp")

        title = title_element.text.strip() if title_element else "Title not found"
        print(title)
        paragraph = paragraph_element.text.strip() if paragraph_element else "Paragraph not found"
        print(paragraph)
        date = date_element.text.strip() if date_element else "Date not found"
        print(date)

        data.append([title, paragraph, date])

# Close the main WebDriver instance
driver.quit()

# Create a DataFrame and save it to a CSV file
df = pd.DataFrame(data, columns=['Title', 'Paragraph', 'Date'])
df.to_csv("abc_news.csv", index=False)
print(df)

