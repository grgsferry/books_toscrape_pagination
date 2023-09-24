import requests
from bs4 import BeautifulSoup
import csv
import time
from random import randint

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

books = []

for i in range(1,51,1):
    URL = f'https://books.toscrape.com/catalogue/page-{i}.html'
    r = requests.get(url=URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('ol', attrs={'class': 'row'})

    for row in table.findAll('li', attrs={'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        book = {}
        book['title'] = row.article.h3.a['title']
        book['price'] = row.article.find('div', attrs={'class': 'product_price'}).find('p', attrs={'price_color'}).text
        book['ratings'] = row.article.find('p', attrs={'class': 'star-rating'})['class'][1]
        book['link'] = row.article.find('div', attrs={'class': 'image_container'}).a['href']

        r_temp = requests.get(url=f'https://books.toscrape.com/catalogue/{book["link"]}', headers=headers)
        soup_temp = BeautifulSoup(r_temp.content, 'html.parser')
        book['availability'] = soup_temp.find('p', attrs={'class': 'instock availability'}).text.strip()

        try:
            book['description'] = soup_temp.findAll('p', attrs={'class': None})[0].text
        except:
            print(f'error getting book {book["link"]}')
            book['description'] = 'no description'

        books.append(book)

    print(f'done scraping page {i}')
    # time.sleep(randint(1,3))
    
filename = 'books_scraped.csv'
with open(filename, 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ['title', 'price', 'ratings', 'link', 'availability', 'description'])
    w.writeheader()
    for book in books:
        w.writerow(book)