import time
from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate

def scrape_questcdn_links(url):
    # Using selenium to open the page and allow JavaScript to load the content
    driver = webdriver.Chrome() # Please downlod chrome if you don't have it or else change the code
    driver.get(url)

    # Allow some time for JavaScript to load the content
    time.sleep(3)

    page_codes = []
    return_details = []

    # Extract data from the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'id': 'table_id'})
    header_row = table.find('thead').find('tr')
    header_columns = header_row.find_all('th')
    headers = [col.text.strip() for col in header_columns]
    quest_number_index = headers.index('Quest Number')

    # Iterate through the rows of the table body
    for row in table.find_all('tr')[2:7]:
        values = []
        columns = row.find_all('td')
        quest_number = columns[quest_number_index].text.strip()
        driver.execute_script(f"prevnext('{quest_number}')")
        
        time.sleep(1)
        
        # Extract the desired table from the new page
        temp_soup = BeautifulSoup(driver.page_source, 'html.parser')
        new_table = temp_soup.find_all('table', {'class': 'table table-borderless posting-table'})
        
        for table in new_table:
            est_value_notes_column = table.find('td', string='Est. Value Notes:')
            if est_value_notes_column:
                est_value_notes_value = est_value_notes_column.find_next('td').text.strip()
                values.append(est_value_notes_value)

            description_column = table.find('td', string='Description:')
            if description_column:
                description_value = description_column.find_next('td').text.strip()
                values.append(description_value)

            closing_date_column = table.find('td', string='Closing Date:')
            if closing_date_column:
                closing_date_value = closing_date_column.find_next('td').text.strip()
                values.append(closing_date_value)

            # You can further process and extract information from the new_table if needed like the following code blocks
            
            # additional_Desc_column = table.find('td', string='Additional Description:')
            # if additional_Desc_column:
            #     additional_Desc_value = additional_Desc_column.find_next('td').text.strip()
            #     values.append(additional_Desc_value)

            # owner_name_column = table.find('td', string='Owner Name:')
            # if owner_name_column:
            #     owner_name_value = owner_name_column.find_next('td').text.strip()
            #     values.append(owner_name_value)


            
        
        return_details.append(values)

    driver.quit()
    return return_details

if __name__ == "__main__":
    target_url = "https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787"
    result = scrape_questcdn_links(target_url)

    if result:
        for i, entry in enumerate(result, start=1):
            print(f"Entry {i}:")

            print("Est. Value Notes: \t",entry[0])
            print("Closing Date: \t\t",entry[1])
            print("Description: \t\t",entry[2])
            # print("Additional Description: \t\t",entry[3])
            # print("Owner Name: \t\t", entry[4])
            print("\n")

