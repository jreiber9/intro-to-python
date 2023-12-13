recipes_list = []

ingredients_list = []

def take_recipe():
    name = str(input("enter your recipe name: "))
    cooking_time = int(input("enter cooking time in mins: "))
    ingredients = input("enter the ingredients: ")

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients.split(', '),
    }

    return recipe

n = int(input("how many recipes would you like to enter: "))

for x in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) <= 4:
        recipe['difficulty'] = 'easy'
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'medium'
    if recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] =  'intermediate'
    if recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'hard'

for recipe in recipes_list:
    print('Recipe: ' + recipe['name'])
    print('Cooking Time (min): ' + str(recipe['cooking_time']))
    print('Ingredients: ')
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print('Difficulty Level: ' + recipe['difficulty'])

def print_ing_list():
    ingredients_list.sort()
    print('Ingredients accross all recipes')
    print('--------------------------------')
    for ingredient in ingredients_list:
        print(ingredient)

print('--------------------------------')

print_ing_list()
    