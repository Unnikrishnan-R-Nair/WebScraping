import time
import jsonlines
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_service_categories(dealer_element):
    service_categories = []
    offer_list = dealer_element.find_element(By.CSS_SELECTOR, ".offerList")
    offer_icons = offer_list.find_elements(By.CSS_SELECTOR, "span[class^='map_spr spr_offer']")

    for icon in offer_icons:
        class_name = icon.get_attribute("class")
        # Mapping service category based on class name
        if "spr_offer1" in class_name:
            service_categories.append("Offer 1 Category")
        elif "spr_offer4" in class_name:
            service_categories.append("Offer 4 Category")
        elif "spr_offer10" in class_name:
            service_categories.append("Offer 10 Category")
        # Add more conditions as needed for other categories
        
    return ', '.join(service_categories)


def get_dealer_data(driver):
    
    dealers = []
    
    dealer_elements = driver.find_elements(By.CSS_SELECTOR, ".location_table tbody tr.ng-scope")
    
   
    for element in dealer_elements:
        dealer = {}
        try:
            dealer['name'] = element.find_element(By.CSS_SELECTOR, "th.ng-binding").text
            dealer_info = element.find_element(By.CSS_SELECTOR, "td.tleft div.ng-binding").text
            dealer['address_phone'] = dealer_info.replace('<br>', ', ')
            dealer['operating_hours'] = element.find_element(By.CSS_SELECTOR, "td.tleft.ng-binding").text
            dealer['service_category'] = get_service_categories(element)
        except Exception as e:
            print(f"Error extracting dealer data: {e}")
        dealers.append(dealer)

    return dealers

def scrape_kia_dealers():
    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    
    # Open Kia Thailand Dealer Locator Page
    driver.get("https://www.kia.com/th/en/shopping-tools/find-a-dealer.html")

    # Wait for the page to load
    time.sleep(3)

    close = driver.find_element(By.CSS_SELECTOR, '.close.notice_agree') or None
    if close:
        driver.execute_script("arguments[0].click();", close)

    all_dealers = []

    page_no = 1
    classes = 'div.pg_num_area div.ng-scope a.pg_num'
    while True:
        try:
            next_button =  driver.find_element(By.CSS_SELECTOR, classes)
        except:
            next_button = None
        print('page no : ', page_no)
        if next_button:
            classes+=" + a.pg_num"
            driver.execute_script("arguments[0].click();", next_button)
            
            time.sleep(3)        
            all_dealers.extend(get_dealer_data(driver))
        else:
            break
        page_no += 1
            

    # Extract dealer data
    # all_dealers.extend(get_dealer_data(driver))

    driver.quit()

    # Save data to JSON Lines file
    with jsonlines.open("unnikrishnan_kia_dealers.jsonl", mode='w') as writer:
        for dealer in all_dealers:
            writer.write(dealer)

if __name__ == "__main__":
    scrape_kia_dealers()


