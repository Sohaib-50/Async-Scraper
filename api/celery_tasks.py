from celery import shared_task
import requests 
from bs4 import BeautifulSoup 
import json
import time


@shared_task
def scrape_task(url, limit=20):
    
    time.sleep(30)
    return {"foo": "bar"}

    
    count_processed = 0
    urls_to_process = {url}
    scraped_contents = {}

    while urls_to_process and count_processed < limit:
        url = urls_to_process.pop()  # get random url to process
        
        response = requests.get(url)
        parsed_response = BeautifulSoup(response.content, 'html.parser')

        page_title = parsed_response.title.text
        scraped_contents[url] = {"page_title": page_title, "headings":[]}
        main_content = parsed_response.find(id="bodyContent")  # main content area of wiki article

        # Extract headings
        for heading in main_content.findAll([f"h{i}" for i in range(1, 7)]):
            heading_level = int(heading.name[1])
            scraped_contents[url]["headings"].append((heading_level, heading.text))

        # Extract links for further exploration
        for link in main_content.findAll("a", href=True):
            href = link["href"]
            
            # only add article links
            if href.startswith("/wiki/") and "File" not in href:
                urls_to_process.add(f"https://en.wikipedia.org{href}")

        count_processed += 1
    
    return scraped_contents
    

# if __name__ == "__main__":
#     url = "https://en.wikipedia.org/wiki/Shaun_Pollock"
#     print(json.dumps(scrape_task(url), indent=4))
