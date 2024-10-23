import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/w/index.php?title=Elon_Musk&diff=1252786351&oldid=1178332503'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.find_all('table')
dataframes = []

# 将提取的表格写入文件
with open('tables_output.txt', 'w', encoding='utf-8') as f:
    for i, table in enumerate(tables):
        f.write(f"Table {i + 1}:\n")
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            cell_data = [cell.text.strip() for cell in cells]
            f.write("\t".join(cell_data) + "\n")
        f.write("\n")

print("提取的表格已写入到 tables_output.txt 文件中。")

'''for table in tables:
    headers = table.find_all('th')
    header_data = [header.text.strip() for header in headers]
    
    rows = table.find_all('tr')
    table_data = []
    
    for row in rows:
        cells = row.find_all(['td', 'th'])
        cell_data = [cell.text.strip() for cell in cells]
        if cell_data:  # 排除空行
            table_data.append(cell_data)

    # 确保数据行的列数与标题列数匹配
    if table_data and len(table_data[0]) == len(header_data):
        df = pd.DataFrame(table_data, columns=header_data)
        dataframes.append(df)

# 打印所有提取的表格
for i, df in enumerate(dataframes):
    print(f"Table {i + 1}:")
    print(df)
    print("\n")'''


#https://en.wikipedia.org/w/index.php?title=Elon_Musk&diff=1252786351&oldid=1178332503