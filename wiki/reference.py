import requests
from bs4 import BeautifulSoup

url1 = 'https://en.wikipedia.org/w/index.php?title=Elon_Musk&oldid=1252786351'
url2 = 'https://en.wikipedia.org/w/index.php?title=Elon_Musk&oldid=1178332503'

def fhj(url):
    # 发送请求
    response = requests.get(url)
    # 解析网页
    soup = BeautifulSoup(response.content, 'html.parser')
    # 找到class为references的元素
    references = soup.find_all(class_='references')
    li_elements = []
    # 提取li中的内容
    for reference in references:
        li_elements.extend(reference.find_all('li'))
    return li_elements

if __name__ == "__main__":

    list1 = [item.get_text() for item in fhj(url1)]
    list2 = [item.get_text() for item in fhj(url2)]

    # 使用集合计算差集
    li_shared = list(set(list1) - set(list2))

    with open('output.txt', 'w', encoding='utf-8') as file:
        for item in li_shared:
            file.write(f"{item}\n")  

    print("列表元素已写入到output.txt文件中。")
