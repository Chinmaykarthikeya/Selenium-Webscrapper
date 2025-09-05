from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time

counter = 0
qury = "laptop"
fl=1

service = Service(r'C:\Users\karth\OneDrive\Desktop\PythonAutomationProjects\myenv\chromedriver.exe')
driver = webdriver.Chrome(service=service)

try:
    # You need to define pg and fl before using them
    
    proxy = "no_proxy"  # placeholder since it's not defined
    
    for page_num in range(1, 21):
        url = f"https://www.flipkart.com/search?q={qury}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_num}"
        driver.get(url)

        # Get elements by class name (adjust selector if needed)
        elems = driver.find_elements(By.CLASS_NAME, "tUxRFH")

        for elem in elems:
            with open(
                f'C:\\Users\\karth\\OneDrive\\Desktop\\PythonAutomationProjects\\myenv\\data\\{qury}_page_{fl}.html',
                'a',
                encoding='utf-8'
            ) as file:
                html = elem.get_attribute('outerHTML')
                if html:
                    file.write(html)
                    print(f"Page {page_num} saved using proxy {proxy}")
                    fl += 1

except requests.exceptions.RequestException as e:
    print(f"failed requests: {e}")

except Exception as e:
    print(f"Error in Selenium: {e}")

time.sleep(5)
driver.quit()
print("Done.")
