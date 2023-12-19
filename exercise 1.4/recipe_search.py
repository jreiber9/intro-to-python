import pickle

def display_recipe(recipe):
    print('Recipe: ', recipe['name'])
    print('Cooking time(in mins): ', recipe['cooking_time'])
    print('Ingredients: ', recipe['ingredients'])
    print('Difficulty: ', recipe['difficulty'])


def search_ingredient(data):
    list_ingredients = list(enumerate(data['all_ingredients']))
    print('Ingredients List: ')
    
    for value in list_ingredients:
        print(value[0], value[1])
    try:
        num = int(input('Enter the number of ingredients you would like to search: '))
        ingredient_searched = list_ingredients[num][1]
        print('searching for', ingredient_searched, '...')
    except ValueError:
        print('Only numbers are allowed!')
    except:
        print('Your number needs to start with at least a value of 1')
    else: 
        for value in data['recipes_list']:
            if ingredient_searched in value['ingredients']:
                print(value)

recipe_file = str(input('please enter file name that contains recipe data: '))

try:
    file = open(recipe_file, 'rb')
    data = pickle.load(file)
    print('file loaded successfully')
except FileNotFoundError:
    print('that file does not exist-exiting.')

else:
    search_ingredient(data)
