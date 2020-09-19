import pandas as pd

data = [
    {'name': 'Akhi', 'age': '23', 'country': 'Indonesia'},
    {'name': 'Nick', 'age': '33', 'country': 'Canada'}
]

df = pd.DataFrame(data)
df.to_csv('results.csv', index=False)
df.to_excel('results.xlsx', index=False)