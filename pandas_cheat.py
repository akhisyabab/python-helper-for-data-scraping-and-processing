import pandas as pd

## WRITING TO CSV OR EXCEL
data = [
    {'name': 'Akhi', 'age': '23', 'country': 'Indonesia'},
    {'name': 'Nick', 'age': '33', 'country': 'Canada'}
]

df = pd.DataFrame(data)
df.to_csv('results.csv', index=False)
df.to_excel('results.xlsx', index=False)

#==================================================================#

## READ CSV OR EXCEL TO LIST DICT
df = pd.read_csv('results.csv')
print(df.to_dict('records'))
df = pd.read_excel('results.xlsx')
print(df.to_dict('records'))