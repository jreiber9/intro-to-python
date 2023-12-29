#importing packages and methods
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

# generating base class for declaritive base
Base = declarative_base()

# creating engine object
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# generating session class, binding to engine
Session = sessionmaker(bind=engine)
# init session object
session = Session()

# defining the recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    # provides string representation of a Recipe object when printed
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"
    
    # prints a well formatted version of recipe
    def __str__(self):
        # starting with empty string to build output format
        output = ""
        # adding recipe details
        output += f"Recipe ID: {self.id}\n"
        output += f"Name: {self.name}\n"
        output += f"Ingredients: {self.ingredients}\n"
        output += f"Cooking Time: {self.cooking_time} in minutes\n"
        output += f"Difficulty: {self.difficulty}\n"
        # outputting line of dashes for seperation
        output += "-"*40 + "\n"
        # returning the formatted string
        return output
    
    # defining calc difficulty method
    def calc_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Hard'

    # defining return ingredients as list method
    def return_ingredients_as_list(self):
        # if list empty
        if self.ingredients == "":
            return []
        # if not use split()
        else:
            return self.ingredients.split(", ")
        
# creating he corresponding table on the db
Base.metadata.create_all(engine)

# create recipe method
def create_recipe():
    # collecting the details
    # validating the recipe name
    while True:
        name = input("Enter the recipe name: ")
        if len(name) > 50:
            print("Error: The name should not exceed 50 characters.")
        else:
            break
    while True:  
        cooking_time_input = input("Enter the cooking time in minutes: ")
        # checking if positive integer
        if not cooking_time_input.isnumeric():
            print("Error: Please enter a valid numeric value for cooking time.")
        else:
            cooking_time = int(cooking_time_input)
            break
    # defining empty ing list
    ingredients_list = []
    # getting number of ingredients
    while True:
        ingredients_input = input("How many ingredients would you like to enter: ")
        # checking for errors
        if not ingredients_input.isnumeric():
            print("Error: Please enter a valid numeric value for number of ingredients.")
        else:
            ingredients_input = int(ingredients_input)
            break

    # uses '_' as variable name since it will not be used in loop
    for _ in range(ingredients_input):
        ingredient = input("Enter an ingredient: ")
        ingredients_list.append(ingredient)
    # converting into a string
    ingredients = ", ".join(ingredients_list)

    # creating a new recipe object
    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time )
    recipe_entry.calc_difficulty()
    # adding the recipe to the db
    session.add(recipe_entry)
    session.commit()

    print("Recipe successfully added!")

# view all recipes function
def view_all_recipes():
    # retrieve all recipes from db
    all_recipes = session.query(Recipe).all()

    # check for entries
    if not all_recipes:
        print("No recipes found!")
        return
    
    # loop and display each recipe
    for recipe in all_recipes:
        print(recipe)


# search by ingredients function
def search_by_ingredients():
    if session.query(Recipe).count() < 1:
        print("No recipes found!")
        return

    # retrieve only ingredients list
    results = session.query(Recipe.ingredients).all()

    # Initialize an empty list called all_ingredients
    all_ingredients = []
    
    # Convert strings into a list and remove duplicates
    for str in results:
        ingredient_list = str[0].split(", ")
        for ingredient in ingredient_list:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)

    # display ingredients to user
    print("Available ingredients:")
    for count, ingredient in enumerate(all_ingredients, start=1):
        print(f"{count}. {ingredient}")

    # ask user input
    corresponding_input = input("Which ingredient(s) do you want to search(corresponding numbers seperate by spaces): ")

    # validate that input
    selected_numbers = corresponding_input.split(" ")
    search_ingredients = []
    for num in selected_numbers:
        if not num.isnumeric():
            print("Input not valid.")
            return
        else:
            num = int(num)
        if num < 1 or num > len(all_ingredients):
            print("Input is not valid.")
            return
        # save if pass into list
        search_ingredients.append(all_ingredients[int(num) - 1])

    # initiating list for filter conditions
    conditions = []

    for search_ingredient in search_ingredients:
        like_term = f"%{search_ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # retrieving the recipes based on the selected ingredients
    matching_recipes = session.query(Recipe).filter(*conditions).all()

    # display matching recipes
    if matching_recipes:
        print("\nMatching Recipes:")
        for recipe in matching_recipes:
            print(recipe)
    else:
        print("\nNo matching recipes found.")


# defining edit recipe method
def edit_recipe():
    # checking for recipes
    if not session.query(Recipe).count():
        print("No recipes found!")
        return
    else:
        # retrieve recipe ids and names
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()

    # display recipes to user
    print("Here are the recipes available to edit:")
    for recipe_id, recipe_name in results:
        print(f"{recipe_id} {recipe_name}")

    # ask user input
    user_input = input("Enter the ID of the recipe you'd like to edit: ")
    # validate input
    if not user_input.isnumeric():
        print("Input is not valid. Please enter numeric value.")
        return
    selected_id = int(user_input)
    # check if ID exists
    if selected_id not in [recipe_id for recipe_id, _ in results]:
        print("Recipe ID not found. Please enter valid ID.")
        return
    # retrieve corresponding recipe to its ID
    recipe_to_edit = session.query(Recipe).get(selected_id)

    # display chosen recipe to user
    print("1 - Name:", recipe_to_edit.name)
    print("2 - Ingredients:", recipe_to_edit.ingredients)
    print("3 - Cooking time", recipe_to_edit.cooking_time)
    
    # user selects attribute to edit
    attribute_choice = input("Enter the number corresponding to the attribute you'd like to edit:")
    # validating the choice
    if not attribute_choice.isnumeric() or int(attribute_choice) < 1 or int(attribute_choice) > 3:
        print("Invalid input. Enter a valid number.")
        return
    # convert valid choice to integer
    chosen_attribute = int(attribute_choice)

    # get new value for attribute from user
    new_value = input("Enter the new value for the selected attribute: ")

    # update the selected attribute with the new value in recipe
    if chosen_attribute == 1:
        if len(new_value) > 50:
            print("Error: Name should not exceed 50 characters.")
            return
        else:
            recipe_to_edit.name = new_value
    elif chosen_attribute == 2:
        # new ingredient(s) to add
        new_ingredients = [ingredient.strip() for ingredient in new_value.split(', ')]
        recipe_to_edit.ingredients.extend(new_ingredients)
    elif chosen_attribute == 3:
        # validating
        if not new_value.isnumeric() or int(new_value) < 0:
            print("Not valid. Please enter a valid numeric value.")
            return
        else:
            recipe_to_edit.cooking_time = int(new_value)
    
    # recalculate diff
    recipe_to_edit.calc_difficulty()

    # committing changes
    session.commit()

# define the delete function
def delete_recipe():
    # check for recipes
    if not session.query(Recipe).count():
        print("No recipes found!")
        return
    else:
        # retrieve ids and names
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    
    # display recipes to user
    print("Here are the recipes available to delete:")
    for recipe_id, recipe_name in results:
        print(f"{recipe_id} {recipe_name}")

    # ask for user input
    user_input = input("Enter the ID of the recipe you'd like to delete:")
    # validating input
    if not user_input.isnumeric():
        print("Input not valid. Please enter numeric value.")
        return
    selected_id = int(user_input)
    # check if ID exists
    if selected_id not in [recipe_id for recipe_id, _ in results]:
        print("Recipe ID not found. Please enter a valid ID.")
        return
    # retreive recipe for ID
    recipe_to_delete = session.query(Recipe).get(selected_id)

    # display the recipe for confirmation
    print("Recipe to delete:")
    print(f"ID: {recipe_to_delete.id}, Name: {recipe_to_delete.name}")

    # asking user for confirmation
    confirmation = input("Are you sure you want to delete this recipe? (yes or no)-").lower()
    if confirmation != "yes":
        print("Deletion cancelled.")
        return
    # delete recipe
    session.delete(recipe_to_delete)
    session.commit()

    print("Recipe successfully deleted!")


# Main Menu loop
while True:
    # Display options
    print("\nMain Menu:")
    print("1. Create a new recipe")
    print("2. View all recipes")
    print("3. Search for recipes by ingredients")
    print("4. Edit a recipe")
    print("5. Delete a recipe")
    print("Type 'quit' to exit the application.")

    # Get user input
    user_choice = input("Enter your choice: ")

    # Check user's choice and call the corresponding function
    if user_choice == "1":
        create_recipe()
    elif user_choice == "2":
        view_all_recipes()
    elif user_choice == "3":
        search_by_ingredients()
    elif user_choice == "4":
        edit_recipe()
    elif user_choice == "5":
        delete_recipe()
    elif user_choice.lower() == "quit":
        # Close session and engine
        session.close()
        engine.dispose()
        print("Exiting the application. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")



    