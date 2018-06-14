import json
from time import sleep
from collections import namedtuple

import requests
from bs4 import BeautifulSoup


def getLinks(url, headers):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('.fixed-recipe-card__h3 a')
    return links



def parseRecipes(u, headers):
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
            calories = calories_section[0].text.replace('cals', '').strip() \
                if calories_section else 0.0

            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if 'Add all ingredients to list' not in ingredient_text and ingredient_text != '':
                        ingredients.append({'step': ingredient.text.strip()})

            description = description_section[0].text.strip().replace('"', '') \
                if description_section else ''

            title = title_section[0].text if title_section else ''

            return json.dumps(Dish(title, description, calories, lipids, carbs, ingredients)._asdict())
    except Exception as ex:
        print('Exception while parsing')
        print(str(ex))
