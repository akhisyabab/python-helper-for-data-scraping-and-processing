from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Example requests with selenium
operating_system = platform.system()
if operating_system == 'Linux':
    driver = webdriver.Chrome('./chromedriver-linux', options=chrome_options)
if operating_system == 'Darwin':
    driver = webdriver.Chrome('./chromedriver-mac', options=chrome_options)
if operating_system == 'Windows':
    driver = webdriver.Chrome('./chromedriver-windows.exe', options=chrome_options)

driver.get('https://www.carfax.com/Service/login')
try:
    WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.CLASS_NAME, "cfx-input-text")))
except:
    raise

driver.find_element_by_name('text').send_keys(email)
driver.find_element_by_name('password').send_keys(cred_password)
driver.find_element_by_xpath('//button[@type="submit"]').click()
wait = WebDriverWait(driver, 30)
wait.until(lambda driver: driver.current_url == 'https://www.carfax.com/Service/garage')

# ============================================================================ #

# find element contain text
driver.find_elements_by_xpath("//*[contains(text(), 'Some text')]")

# ============================================================================ #

# Add cookies from Export cookie JSON file for Puppeteer extension
# https://chrome.google.com/webstore/detail/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppet/nmckokihipjgplolmcmjakknndddifde/related
driver.get('https://www.site.com')
with open('www.site.com.cookies.json') as json_file:
    cookies = json.load(json_file)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https://www.site.com')
