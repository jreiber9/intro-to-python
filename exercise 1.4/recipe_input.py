import pickle


def take_recipe():
    name = str(input("enter your recipe name: "))
    cooking_time = int(input("enter cooking time in mins: "))
    ingredients = input("enter the ingredients: ")
    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients.split(', '),
        'difficulty': difficulty,
    }

    return recipe

def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = 'easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = 'medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty =  'intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = 'hard'
    return difficulty



filename = input('Enter filename to import: ')

try:
    file = open(filename, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    print('File doesnt exist - creating a blank one.')
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    print('An unexpected error occured')
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']
    print('Creating')

n = int(input('How many recipes would you like to enter?: '))

for x in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)
    print('recipe added successfully')


data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

new_file = open(filename, 'wb')
pickle.dump(data, new_file)
new_file.close()
print('the recipe file has been updated!')