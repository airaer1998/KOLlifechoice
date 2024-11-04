from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import logging
import os
from scrapegraphai.graphs import SmartScraperGraph
import json

#爬取url链接函数
def save_external_links(url, output_file):

    resp = urlopen(url).read().decode("utf-8")
    soup = bs(resp, "html.parser")
    
    external_links = soup.find_all('a', class_='external text', href=True)
    
    with open(output_file, "w", encoding="utf-8") as file:
        for link in external_links:
            output_line = f"{link['href']}\n"
            file.write(output_line)
    
    print(f"结果已保存到 {output_file}")


#对比url的不同函数
def extract_unique_urls(file1, file2, output_file):

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        urls1 = set(f1.read().splitlines())
        urls2 = set(f2.read().splitlines())
    
    unique_urls = urls1 - urls2
    
    with open(output_file, 'w') as f_out:
        for url in unique_urls:
            f_out.write(url + '\n')




def process_urls_from_file(api_key, file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        links_list = [line.strip() for line in file]

    graph_config = {
        "llm": {
            "api_key": api_key,
            "model": "gpt-4o-mini", 
        },
    }
    #links_list = links_list[:10] #test
    num = 0
    for link in links_list:
        try:
            prompt = (
            '''
            Please extract key information from the following webpage and output it in JSON format.
            Ensure the JSON structure matches the following format:
            { 
                "summary": [ 
                    { 
                        "action": "Brief description of the action",
                        "details": "Detailed information about the action"
                    },
                ]
            }

            If any information is missing, please fill the relevant fields with "NA".
            Ensure the output is valid JSON without any extra explanations.
            '''
            )
            smart_scraper_graph = SmartScraperGraph(
                prompt=prompt,
                source=link,
                config=graph_config
            )
            result = smart_scraper_graph.run()
            output = json.dumps(result, indent=2)
            data = json.loads(output)
            data["url"] = link
            output = json.dumps(data, indent=2)
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(output)
            num+=1
            print(f"N0.{num} {link} is OK\n")
        except Exception as e:
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(f"An error occurred for URL {link}: {e}\n")
    print(f"All results saved to {output_file}")

if __name__ == "__main__":

    OPENAI_API_KEY = "****"
    #两版对比url
    
    save_external_links(
        "https://en.wikipedia.org/w/index.php?title=Elon_Musk&oldid=1178332503",
        "elon_musk_external_links_2023.txt"
    )
    save_external_links(
        "https://en.wikipedia.org/w/index.php?title=Elon_Musk&oldid=1255043438",
        "elon_musk_external_links.txt"
    )
    extract_unique_urls('elon_musk_external_links.txt', 'elon_musk_external_links_2023.txt', 'output.txt')
    file_path = "output.txt"  
    output_file = "all_results.json"  
    process_urls_from_file(OPENAI_API_KEY, file_path, output_file)

    



