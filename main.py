import re
import json
from pathlib import Path

from src.parse import parse_data, URL
from src.seeds import add_author, add_quote
import src.connect
from src.models import Authors, Quotes

AUTHORS = 'json/authors.json'
QUOTES = 'json/quotes.json'

def user_interface():
    while True:
        input_cmd = input("Enter the command: ")
        
        if input_cmd.lower() == "exit":
            break

        try:
            cmd, args = re.split(":", input_cmd)
        except Exception as e:
            print("I don't understand you")
            continue

        if cmd.lower() == "name":
            try:
                author = Authors.objects.get(fullname = args)
            except Exception as e:
                print(e)
                continue
            
            quotes = Quotes.objects(author = author.id)
            for quote in quotes:
                print(quote.quote)

        elif cmd.lower() == "tag":
            quotes = Quotes.objects(tags__name=args)
            for quote in quotes:
                print(quote.quote)
        elif cmd.lower() == "tags":
            tags = re.split(",", args)
    
            quotes = Quotes.objects(tags__name__in=tags)
            for quote in quotes:
                print(quote.quote)
        else:
            print("I don't understand you")

def parse_to_json():
    quotes, authors = parse_data(URL)

    with open('json/quotes.json', 'w') as file:
        json.dump(quotes, fp=file)
    with open('json/authors.json', 'w') as file:
        json.dump([*authors.values()], fp=file)

def dump_json_to_db():
    with open(AUTHORS) as file:
        authors = json.load(file)
    for author in authors:
        add_author(author)

    with open(QUOTES) as file:
        qoutes = json.load(file)
    for qoute in qoutes:
        add_quote(qoute)
    print("[*]Upload data to database")

def main():
    if (
        not Path(AUTHORS).exists() or
        not Path(QUOTES).exists()):
        parse_to_json()
        dump_json_to_db()

    user_interface()

if __name__ == "__main__":
    main()