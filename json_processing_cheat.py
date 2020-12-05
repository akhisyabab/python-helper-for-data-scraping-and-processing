import json

# WRITING TO JSON FILE
data = {
    'name': 'Akhi',
    'age': '23',
    'country': 'Indonesia'
}
with open('results.json', 'w') as outfile:
    json.dump(data, outfile)

# ========================================== #

# READING FROM JSON FILE
import json
with open('results.json') as json_file:
    data = json.load(json_file)

print(data)


# ========================================== #

# READING FROM FOLDER
import glob
files = sorted(glob.glob('./folder_name/*.json'),key=lambda x:float(re.findall("(\d+)",x)[0]))
all_datas = []
for file in files:
    print(file)
    with open(file) as json_file:
        datas = json.load(json_file)
    all_datas.append(datas)


# ========================================== #

# READING FROM HTML SCRIPT
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('res.html'), 'html.parser')

scripts = soup.find_all('script')
selected_script = None
for script in scripts:
    if 'window.__APOLLO_STATE__=' in str(script):
        selected_script = script

selected_script = selected_script.text
selected_script = selected_script.replace('window.__APOLLO_STATE__=', '').replace(';', '')
converted_script = json.loads(selected_script)

with open('converted_script.json', 'w') as outfile:
    json.dump(converted_script, outfile)