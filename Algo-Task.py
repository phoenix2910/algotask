from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

# Set up the Chrome WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", False)
    #chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

# Get the Wikipedia table from the webpage
def get_wikipedia_table(driver):
    table_xpath = "(//h3[@id='1_000_000+_articles']/following::table/tbody)[1]"
    header_elements = driver.find_elements(By.XPATH, "(//h3[@id='1_000_000+_articles']/following::table/thead)[1]//th")
    column_names = [header.text for header in header_elements]
    
    # Extract rows directly without waiting
    rows = driver.find_elements(By.XPATH, table_xpath + '/tr')
    data = [[cell.text for cell in row.find_elements(By.XPATH, './td')] for row in rows]
    
    df = pd.DataFrame(data, columns=column_names)
    driver.quit()
    return df

# Calculate the total number of articles for the given languages
def findTotalArticlesByLanguages(df, languages):
    languages = [lang.lower() for lang in languages]  # Case-insensitive matching
    
    # Filter and clean the 'Articles' column, then calculate the sum
    df['Language'] = df['Language'].str.lower()  # Make language column lowercase
    filtered_df = df[df['Language'].isin(languages)].copy()  # Make a copy to avoid modifying the original
    
    # Remove commas and convert to numeric in the 'Articles' column
    filtered_df['Articles'] = filtered_df['Articles'].replace({',': ''}, regex=True)
    filtered_df.loc[:, 'Articles'] = pd.to_numeric(filtered_df['Articles'], errors='coerce')  # Use .loc to avoid SettingWithCopyWarning
    
    total_articles = filtered_df['Articles'].sum()
    print(f"Total Articles for specified languages: {total_articles}")

# Main function
def main():
    driver = setup_driver()
    driver.get("https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table")
    
    # Take user input for languages
    # user_input = input("Enter the languages (separate by commas, e.g., English,French,Spanish): ")
    #languages_to_extract = [lang.strip() for lang in user_input.split(",")]
    languages_to_extract = ["English","Germany"]
    df = get_wikipedia_table(driver)
    findTotalArticlesByLanguages(df, languages_to_extract)

if __name__ == "__main__":
    main()
