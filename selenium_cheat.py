# find element contain text
driver.find_elements_by_xpath("//*[contains(text(), 'Some text')]")


# Add cookies from Export cookie JSON file for Puppeteer extension
# https://chrome.google.com/webstore/detail/%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BCjson%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%87%BA%E5%8A%9B-for-puppet/nmckokihipjgplolmcmjakknndddifde/related
driver.get('https://www.site.com')
with open('www.site.com.cookies.json') as json_file:
    cookies = json.load(json_file)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https://www.site.com')
