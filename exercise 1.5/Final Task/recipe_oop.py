class Recipe(object):
    # this is a class variable
    all_ingredients = []

    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None

    # method calculates difficulty
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty =  'intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = 'hard'

    # method gets diff
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    # getter and setter for 'name'
    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    # getter method for ingredients
    def get_ingredients(self):
        return self.ingredients
    
    # search method for ingredients
    def search_ingredients(self, ingredient):
        return ingredient in self.get_ingredients()

    # checks for dulpicate ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not self.search_ingredients(ingredient):
                Recipe.all_ingredients.append(ingredient)

    # adds multiple ingredients calls update method to check dupes
    def add_ingredients(self, *args):
        self.ingredients += args
        # calls the method to update
        self.update_all_ingredients()

    # string method
    def __str__(self):
        return f"\nRecipe Name: {self.name}\nIngredients: {','.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.get_difficulty()}\n"

    

def recipe_search(data, search_term):
    for recipe in data:
        if recipe.search_ingredients(search_term):
            print(recipe)


# creating recipes
tea = Recipe('tea', ['tea leaves', 'sugar', 'water'], 5)
coffee = Recipe('coffee', ['coffee powder', 'sugar', 'water'], 5)
cake = Recipe('cake', ['sugar', 'butter', 'eggs', 'vanilla essence', 'flour', 'baking powder', 'milk'], 50)
banana_smoothie = Recipe('banana smoothie', ['bananas', 'milk', 'peanut butter', 'sugar', 'ice cubes'], 5)

# list of the recipes
recipe_list = [tea, coffee, cake, banana_smoothie]

# displaying the string representation
for recipe in recipe_list:
    print(recipe)

# search for recipes that include certain ingredients
ingredients_to_search = ['water', 'sugar', 'bananas']

for certain in ingredients_to_search:
    print(f"Recipes containing {certain}:")
    recipe_search(recipe_list, certain)
    print('\n')
