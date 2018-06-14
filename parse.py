import json
import logging
from time import sleep
from collections import namedtuple

import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='salads', body=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False



def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def parse(u):
    ingredients = []
    fields = ['title', 'description', 'calories', 'lipids', 'carbs', 'ingredients']
    Dish = namedtuple('Dish', fields)

    try:
        r = requests.get(u, headers=headers)

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            title_section = soup.select('.recipe-summary__h1')
            description_section = soup.select('.submitter__description')
            ingredients_section = soup.select('.recipe-ingred_txt')
            calories_section = soup.select('.calorie-count')
            carbs = soup.find(itemprop="carbohydrateContent").get_text()
            lipids = soup.find(itemprop="proteinContent").get_text()
            if calories_section:
                calories = calories_section[0].text.replace('cals', '').strip()

            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text and ingredient_text != '':
                        ingredients.append({'step': ingredient.text.strip()})
            if description_section:
                description = description_section[0].text.strip().replace('"', '')

            if title_section:
                title = title_section[0].text

            return json.dumps(Dish(title, description, calories, lipids, carbs, ingredients)._asdict())
    except Exception as ex:
        print('Exception while parsing')
        print(str(ex))

def create_index(es_object, index_name):
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "salads": {
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "calories": {
                        "type": "float"
                    },
                    "lipids": {
                        "type": "float"
                    },
                    "carbs": {
                        "type": "float"
                    },
                    "ingredients": {
                        "type": "nested",
                        "properties": {
                            "step": {"type": "text"}
                        }
                    },
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }
    logging.basicConfig(level=logging.ERROR)
    es = connect_elasticsearch()
    create_index(es, 'recipes')
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('.fixed-recipe-card__h3 a')
        for link in links:
            sleep(2)
            result = parse(link['href'])
            print(result)
            if es is not None:
                create_index(es, 'recipes')
                out = store_record(es, 'recipes', result)
                print('Data indexed successfully')
            print('=================================')
