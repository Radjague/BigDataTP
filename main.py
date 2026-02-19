import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

keywords = [
    "iot", "sensor", "smart", "embedded",
    "arduino", "raspberry", "monitoring",
    "wireless", "telemetry"
]

headers = {"User-Agent": "Mozilla/5.0"}

datasets = []
target = 2000

for keyword in keywords:
    page = 1
    
    while len(datasets) < target:
        print(f"Keyword: {keyword} | Page: {page}")
        
        url = f"https://catalog.data.gov/dataset?q={keyword}&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("h3", class_="dataset-heading")
        
        if not results:
            break
        
        for result in results:
            title = result.text.strip()
            link = result.find("a")["href"]
            
            datasets.append({
                "Keyword": keyword,
                "Title": title,
                "URL": "https://catalog.data.gov" + link
            })
            
            if len(datasets) >= target:
                break
        
        page += 1
        time.sleep(1)

    if len(datasets) >= target:
        break

df = pd.DataFrame(datasets)
df.drop_duplicates(subset=["Title"], inplace=True)
df.to_csv("iot_datasets_2000.csv", index=False)

print("Done!")
print("Total collected:", len(df))
