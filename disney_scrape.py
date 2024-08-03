from tabnanny import check
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=service, options=options)

# URL of the Disney World hotel rates page
url = 'https://disneyworld.disney.go.com/resorts/'

# Open the webpage
driver.get(url)

 # Allow the page to load completely
time.sleep(5)  # Adjust sleep time as necessary

checkin_dates = ["10/01/2024", "10/02/2024", "10/03/2024", "10/04/2024", "10/05/2024", "10/06/2024", 
 "10/07/2024", "10/08/2024", "10/09/2024", "10/10/2024", "10/11/2024", "10/12/2024", 
 "10/13/2024", "10/14/2024", "10/15/2024", "10/16/2024", "10/17/2024", "10/18/2024", 
 "10/19/2024", "10/20/2024", "10/21/2024", "10/22/2024", "10/23/2024", "10/24/2024", 
 "10/25/2024", "10/26/2024", "10/27/2024", "10/28/2024", "10/29/2024", "10/30/2024", "10/31/2024"]



checkout_dates = ["10/02/2024", "10/03/2024", "10/04/2024", "10/05/2024", "10/06/2024", 
 "10/07/2024", "10/08/2024", "10/09/2024", "10/10/2024", "10/11/2024", "10/12/2024", 
 "10/13/2024", "10/14/2024", "10/15/2024", "10/16/2024", "10/17/2024", "10/18/2024", 
 "10/19/2024", "10/20/2024", "10/21/2024", "10/22/2024", "10/23/2024", "10/24/2024", 
 "10/25/2024", "10/26/2024", "10/27/2024", "10/28/2024", "10/29/2024", "10/30/2024", "10/31/2024", "11/01/2024"]


# Create a list to store the data
data = []

def pop_check():
    #check for pop chat invite and reject it
    try:
        inviteReject = driver.find_element(By.ID, 'inviteReject')
        inviteReject.click()
    except:
        print("not chat invite")


for date_index in range(0, len(checkin_dates)):
    checkin = checkin_dates[date_index]
    checkout = checkout_dates[date_index]


    # Find and interact with the date fields by 'name'
    checkin_field = driver.find_element(By.NAME, 'checkInDate')
    checkin_field.clear()
    time.sleep(1)
    checkin_field.send_keys(checkin)
    time.sleep(1)
    pop_check()

    checkout_field = driver.find_element(By.NAME, 'checkOutDate')
    checkout_field.clear()
    time.sleep(1)
    checkout_field.send_keys(checkout)
    time.sleep(1)
    pop_check()

    checkout_field = driver.find_element(By.NAME, 'checkOutDate')
    checkout_field.clear()
    time.sleep(1)
    checkout_field.send_keys(checkout)
    time.sleep(1)
    pop_check()

    search_button = driver.find_element(By.NAME, 'findRoomButton')
    search_button.click()
    try:
        time.sleep(0.3)
        search_button.click()
    except:
        print("stale double click")

    pop_check()

    # Allow the results to load
    time.sleep(10)  # Adjust sleep time as necessary
    pop_check()

    # Find the relevant section containing hotel room rates
    # Note: The actual selectors will vary based on the website's structure
    hotels = driver.find_elements(By.CLASS_NAME, 'resortCardLink')

    print(len(hotels))
    # Extract the necessary information
    for hotel in hotels:
        try:
            name = hotel.find_element(By.CLASS_NAME, 'cardName').text.strip()
            rate = hotel.find_element(By.CLASS_NAME, 'bestValuePrice').text.strip()  # Example class name, adjust as needed
            data.append({'Hotel': name, 'Rate': rate, 'Price': rate.split('\n')[1], 'CheckIn': checkin, 'CheckOut': checkout})
            print({'Hotel': name, 'Rate': rate, 'Price': rate.split('\n')[1], 'CheckIn': checkin, 'CheckOut': checkout})
        except: 
            print("failed")


print(data)

# Convert to a DataFrame
df = pd.DataFrame(data)
print(df)
df.to_csv("ouptut_oct.csv")

# Close the WebDriver
driver.quit()