import requests
import csv
import json


URL = 'https://quotes.toscrape.com/api/quotes?page='

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

scraped_quotes = []
page = 0
has_next = True

while has_next:    
    page += 1

    r = requests.get(url=f'{URL}{page}', headers=headers)
    result = json.loads(r.content)
    quotes = result['quotes']

    for i in range(len(quotes)):
        quote = {}
        quote['author'] = quotes[i]['author']['name']
        quote['tags'] = quotes[i]['tags']
        quote['text'] = quotes[i]['text']
        scraped_quotes.append(quote)

    has_next = result['has_next']
    print(f'done scraped page {page}')

filename = 'infinite_quotes_scraped.csv'
with open(filename, 'w', newline='', encoding="ascii", errors='ignore') as f:
    w = csv.DictWriter(f, ['author', 'tags', 'text'])
    w.writeheader()
    for quote in scraped_quotes:
        w.writerow(quote)