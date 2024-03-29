import json

import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com"

def parse_data_author(fullname: str, url: str):
    html_doc = requests.get(url)

    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        description = soup.find('div', class_='author-description')

        author = {
            "fullname": fullname,
            "born_date": born_date.text,
            "born_location": born_location.text,
            "description": description.text
        }

        return author


def parse_data(url: str):
    authors = {}
    quotes = []

    html_doc = requests.get(url)

    if html_doc.status_code == 200:
        print(f"[*] Parse url: {url}")
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        quotes_ = soup.find_all('div', class_='quote')
        for quote_ in quotes_:
            author = quote_.find('small', class_='author')
            quote = quote_.find('span', class_='text')
            tags = quote_.find_all('a', class_='tag')

            quotes.append({
                'author': author.text,
                'quote': quote.text,
                'tags': [tag.text for tag in tags]
            })

            link_author = quote_.find('a')
            url_author = f"{URL}{link_author['href']}"
            
            author_ = parse_data_author(fullname= author.text, url=url_author)
            authors.update({author.text: author_})

        next_buttom = soup.find('li', class_='next')

        if next_buttom:
            link_next_page = next_buttom.find('a')['href']
            qt, at = parse_data(f"{URL}{link_next_page}")
            quotes.extend(qt)
            authors.update(at)

    return quotes, authors


if __name__ == "__main__":
    quotes, authors = parse_data(URL)

    with open('json/quotes.json', 'w') as file:
        json.dump(quotes, fp=file)

    with open('json/authors.json', 'w') as file:
        json.dump(authors, fp=file)