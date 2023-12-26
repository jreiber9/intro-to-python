import mysql.connector

# initializing connectioin to conn
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

# intializing cursor object from conn
cursor = conn.cursor()

# creating database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# to use certain database
cursor.execute("USE task_database")

# creating the recipe table
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
               )
               ''')

# Main Menu 
def main_menu(conn, cursor):
    while True:
        # Display menu options
        print("\nMain Menu:")
        print("1. Add Recipe")
        print("2. Search Recipes")
        print("3. Update Recipe")
        print("4. Delete Recipe")
        print("5. Exit")

        # Get user choice
        choice = input("Enter your choice (1-5): ")

        # Call the respective function based on user input
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            # Commit changes and close the connection before exiting
            conn.commit()
            conn.close()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Create Recipe Method
def create_recipe(conn, cursor):
    # collecting recipe details
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients (comma-seperated): ").split(', ')

    # calculate difficulty
    difficulty = calc_difficulty(cooking_time, ingredients)

    # converting the ingredients list to comma seperated string
    ingredients_str = ", ".join(ingredients)

    # building sql query to insert recipe
    sqlquery = f"INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    values = (name, ingredients_str, cooking_time, difficulty)
    # executing the query
    cursor.execute(sqlquery, values)

    # commit the changes
    conn.commit()

    print("Recipe added successfully!")

# Calculate difficulty
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        return 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        return  'Intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return 'Hard'


# Search Recipe method
def search_recipe(conn, cursor):
    # getting list of ingredients from table
    cursor.execute("SELECT DISTINCT ingredients from Recipes")
    results = cursor.fetchall()

    print("\nAvailable ingredients: ")

    all_ingredients = []

    # extracting ingredients from resullts using a for loop
    for result in results:
        ingredients = result[0].split(', ')
        all_ingredients.extend(ingredients)

    # removing duplicates by converting to set then back to list
    set_ingredients = set(all_ingredients)
    all_ingredients = list(set_ingredients)

    # displaying ingredients with numbers enumerating
    for item, ingredient in enumerate(all_ingredients, 1):
        print(f"{item}. {ingredient}")

    # user choosing ingredient
    search_ingredient = input("Enter the corresponding number of the ingredient you want to search: ")

    # testing to be sure user input is valid
    try:
        search_ingredient_number = int(search_ingredient)
        if 1<= search_ingredient_number <= len(all_ingredients):
            # get the selected ingredient
            selected_ingredient = all_ingredients[search_ingredient_number - 1]

            # build sql query to search for recipes with selected
            query = f"SELECT * FROM Recipes WHERE ingredients LIKE '%{selected_ingredient}%'"

            # execute query
            cursor.execute(query)

            # fetching results
            search_results = cursor.fetchall()

            # displaying results
            print("\nSearch Results: ")
            for result in search_results:
                print(f"Recipe ID: {result[0]}, Name: {result[1]}, Cooking Time: {result[3]} minutes, Difficulty: {result[4]}")

        else:
            print("Input not valid, please enter a valid number.")
    
    except ValueError:
        print("Input not valid, please enter a valid number.")

# Update recipe
def update_recipe(conn, cursor):
    while True:
        # fetching existing recipes
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()

        print("\nExisting Recipes:")
        for result in results:
            print(f"Recipe ID: {result[0]}, Name: {result[1]}, Cooking Time: {result[3]} minutes, Difficulty: {result[4]}")
        print("Enter '0' to return to the Main Menu.")
        # user input for recipe to update
        recipe_id = input("Enter the ID of the recipe you want to update: ")

        try:
            recipe_id = int(recipe_id)
            if recipe_id == 0:
                break
            # fetching the recipe
            cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
            selected_recipe = cursor.fetchone()

            if selected_recipe:
                print("\nSelected Recipe:")
                print(f"Recipe ID: {selected_recipe[0]}, Name: {selected_recipe[1]}, Cooking Time: {selected_recipe[3]} minutes, Difficulty: {selected_recipe[4]}")

                # user selects the column
                column = input("Enter which you want to update (name, cooking_time, ingredients): ").lower()

                if column in ('name', 'cooking_time', 'ingredients'):
                    # user input for new value
                    new_value = input(f"Enter the new value for {column}: ")

                    # updates the recipe
                    update_query = f"UPDATE Recipes SET {column} = %s WHERE id = %s"
                    cursor.execute(update_query, (new_value, recipe_id))

                    # Recalculate difficulty if updating cooking_time or ingredients
                    if column in ('cooking_time', 'ingredients'):
                        # Recalculate difficulty and update the difficulty column
                        difficulty = calc_difficulty(selected_recipe[3] if column == 'cooking_time' else int(new_value),
                                                    selected_recipe[2] if column == 'ingredients' else new_value)
                        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))

                    # commiting changes
                    conn.commit()
                    print(f"Recipe with ID {recipe_id} updated successfully.")
                else:
                    print("Invalid column. Please enter a valid column name.")
            else:
                print("Recipe not found. Please enter a valid recipe ID.")

        except ValueError:
            print("Invalid input. Please enter a valid ID.")


# Delete recipe
def delete_recipe(conn, cursor):
    # fetch existing recipes
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    print("Existing Recipes:")
    for result in results:
        print(f"Recipe ID: {result[0]}, Name: {result[1]}, Cooking Time: {result[3]} minutes, Difficulty: {result[4]}")

    recipe_id = input("Enter the ID of the recipe you want to delete: ")

    try:
            recipe_id = int(recipe_id)
            # Step 3: Confirm Deletion
            confirmation = input(f"Are you sure you want to delete the recipe with ID {recipe_id}? (yes/no): ").lower()
            
            if confirmation == 'yes':
                # Step 4: Delete the Recipe
                delete_query = "DELETE FROM Recipes WHERE id = %s"
                cursor.execute(delete_query, (recipe_id,))

                # Step 5: Commit Changes
                conn.commit()
                print(f"Recipe with ID {recipe_id} deleted successfully.")
            else:
                print("Deletion canceled.")

    except ValueError:
        print("Input not valid, please enter a valid ID.")



# calling main menu into main code
main_menu(conn, cursor)