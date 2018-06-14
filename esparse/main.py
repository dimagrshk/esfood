from time import sleep

from parse import getLinks, parseRecipes
from estack import connect_elasticsearch, create_index, store_record

def getNstore():
    es = connect_elasticsearch()
    create_index(es, 'recipes')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    links = getLinks(url=url, headers=headers)

    for link in links:
        sleep(2)
        result = parseRecipes(link['href'], headers)
        print(result)
        out = store_record(es, 'recipes', result)
        print(out)
        print('=================================')

if __name__ == '__main__':
    getNstore()
