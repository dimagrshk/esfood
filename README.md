# esfood
Parsing recipes from [allrecipes](https://www.allrecipes.com/) of salads, desserts etc. and store it in Elasticsearch index.

## Usage
run `setup.py` then:
`python3 esparse/main -u https://www.allrecipes.com/recipes/96/salad/`

## Example of object in ES index
```
{
        "_index": "recipes",
        "_type": "salads",
        "_id": "FDDq_WMBrPKEZTKfe6ba",
        "_score": 1,
        "_source": {
          "title": "Quinoa Salad with Grapefruit, Avocado, and Arugula",
          "description": "Intriguing combination of quinoa, arugula, dried cranberries, avocado and grapefruit with a spicy dressing make this a snazzy side dish or lovely summer lunch main dish.",
          "calories": "427",
          "lipids": "8.4",
          "carbs": "49.5",
          "ingredients": [
            {
              "step": "1 cup quinoa"
            },
            {
              "step": "4 cups water"
            },
            {
              "step": "1/4 teaspoon salt"
            },
            {
              "step": "1/4 cup dried cranberries"
            },
            {
              "step": "1/4 cup fresh lime juice"
            },
            {
              "step": "1/4 cup olive oil"
            },
            {
              "step": "2 teaspoons honey"
            },
            {
              "step": "2 cloves garlic, minced"
            },
            {
              "step": "1 teaspoon minced serrano pepper"
            },
            {
              "step": "1/4 cup chopped fresh mint"
            },
            {
              "step": "1/4 cup minced cilantro"
            },
            {
              "step": "1 shallot, minced"
            },
            {
              "step": "1/2 cup arugula"
            },
            {
              "step": "1 pinch salt and black pepper to taste"
            },
            {
              "step": "4 cups baby arugula leaves, washed and dried"
            },
            {
              "step": "1 avocado - peeled, pitted and diced"
            },
            {
              "step": "1/2 grapefruit, peeled and sectioned"
            }
          ]
        }
      }
```
