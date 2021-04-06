import sqlite3
import json
import random

class Model:
    connection  = sqlite3.connect('mealplan.db')
    cursor = connection.cursor() 
    
    #the meal_list has to be string because sqlite cannot store list datatype
    #then using the json library to deserialize the meal list into string type

    command_createUserInfo = '''
        CREATE TABLE IF NOT EXISTS 
        UserInfo(ID INTEGER PRIMARY KEY AUTOINCREMENT, nutrition_standard TEXT, height INTEGER, weight INTEGER, age INTEGER, meal_list TEXT)
    ''' 

    command_createUserDefinedMeal = ''' 
        CREATE TABLE IF NOT EXISTS
        UserDefinedMeal(meal_name TEXT, start_time TEXT, end_time TEXT, 
                        set_of_dishes TEXT, nutritious_retriction TEXT, 
                        regular BOOLEAN, flexible BOOLEAN)
    ''' 

    command_createRecipe = '''
        CREATE TABLE IF NOT EXISTS
        Recipe(recipe_name TEXT, serving_size INTEGER, cooking_time INTEGER, tag TEXT,
                ingredient_name TEXT, amount FLOAT, nutrition_name TEXT,
                energy FLOAT, steps_taken TEXT)
    '''

    cursor.execute(command_createUserInfo)
    cursor.execute(command_createUserDefinedMeal) 
    cursor.execute(command_createRecipe)

    connection.commit()

    def __init__(self):
        pass

    def set_user_info(UserInfo):
        """ 

​	*This function stores the user's information from survey to the meal plan database.* 
​	@parameters:
​				UserInfo: a dictionary containing the user's basic information
​   *Database: UserInfo*
​	@column:
​			    nutrition_standard: String: the user's standard for nutrition
​    			height: Integers: user's height
​    			weight: Integers: user's weight
​    			age: Integers: user's age
​    			meal_list: List [String]: a list of meals
​	@return: none
​    """ 
        nutrition_standard = UserInfo['nutrition_standard']
        height = UserInfo['height']
        weight = UserInfo['weight']
        age = UserInfo['age']
        meal_list = UserInfo['meal_list']

        meal_list = json.dumps(meal_list) #convert into str type
        Model.cursor.execute('''INSERT INTO UserInfo(nutrition_standard, height, weight, age, meal_list)
                        VALUES (?, ?, ?, ?, ?)''',
                        (nutrition_standard, height, weight, age, meal_list)) 

        Model.connection.commit()

    def get_user_info():
        """
​	    *This function fetches the latest update of the user's information from the database*
​	    @parameters: none
​	    @return: data: a list of the user's attributes
        """
        Model.cursor.execute(''' SELECT * FROM UserInfo ORDER BY ID DESC LIMIT 1''' )  
        data = Model.cursor.fetchone()
        Model.connection.commit()

        return data 

    def set_user_nutritious_restriction():
        """
        To be determined
        """
        pass

    def get_user_nutritious_restriction():
        """
        To be determined
        """
        pass

    def set_user_defined_meal(UserDefinedMeal):
        """ 
​       *This function store the user's pre-defined meal to the meal plan database* 
​       @parameters:
                UserDefinedMeal: a dictionary containing the attributes of a defined meal
​       *Database: UserDefinedMeal* 
​       @column:
                name: String: the name of the meal
                start_time: String (ex "12:00"): the meal starting time 
                end_time: String (ex "12:00"): the meal end time
                set_of_dishes: String: the types of dishes in this meal
                nutritious_restriction: To be determined #string
                regular: Boolean: true or false
                flexible: Boolean: true or false
​	    @return: none

​       """

        meal_name = UserDefinedMeal['meal_name']
        time = UserDefinedMeal['time']
        set_of_dishes = UserDefinedMeal['set_of_dishes']
        nutritious_restriction = UserDefinedMeal['nutritious_restriction']
        regular = UserDefinedMeal['regular']
        flexible = UserDefinedMeal['flexible']

        start_time = str(time[0]) + ":" + str(time[1])
        end_time = str(time[2]) + ":" + str(time[3])

        set_of_dishes = json.dumps(set_of_dishes) #serialize list datatype

        Model.cursor.execute('''INSERT INTO UserDefinedMeal
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (meal_name, start_time, end_time, set_of_dishes,
                        nutritious_restriction, regular,flexible)) 

        Model.connection.commit() 
        

    def get_user_defined_meal_names():
        """
​	    *This function returns the meal names from the user's defined meals database*
​	    @parameters: none
​	    @return: data
​	    """ 
        # return list of Meal Names in UserDefinedMeal db
        Model.cursor.execute(''' SELECT * FROM UserDefinedMeal''' )  
        data = Model.cursor.fetchall()
        Model.connection.commit()

        return data


    def get_user_defined_meal(meal_name):
        """
​	    *This function gets the attributes of the meal from the database based on its name*
​	    @parameters: meal_name (string): the name of the meal
​	    @return: a tuple contains the information of meal_name, start_time, end_time, set_of_dishes, nutritious_restriction, regular, flexible 
​	    """ 

        Model.cursor.execute('''SELECT * FROM UserDefinedMeal
                                WHERE meal_name = (?)''', (meal_name,))
        data = Model.cursor.fetchall()
        Model.connection.commit()

        return data

    def set_recipe(Recipe):
        """ 
​       *This function stores a new recipe to the recipe database* 
​       @parameters:
                Recipe: a dictionary containing the attributes of the recipe
​       *Database: Recipe* 
​       @column:
                recipe_name: String: the name of the recipe
                serving_size: Integer: the scale of the serving recipe
                cooking_time: Integer: the required to cook this recipe 
                tag: String category of the recipe 
                ingredient_name: String the ingredients contained in the recipe 
                amount: Float: the amount of the ingredient
                nutrition_name: String: the name of the nutrition
                energy: Float: the amount of energy for that meal
                steps_taken: String: method to cook the recipe 
​	    @return: none
​       """ 
        recipe_name = Recipe['recipe_name']
        serving_size = Recipe['serving_size']
        cooking_time = Recipe['cooking_time']
        tag = Recipe['tag']
        ingredients = Recipe['ingredients']
        nutritions = Recipe['nutritions']
        steps_taken = Recipe['steps_taken']

        ingredient_name = ingredients[0]
        amount = ingredients[1]  
        nutrition_name = nutritions[0] 
        energy = nutritions[1]  

        Model.cursor.execute('''INSERT INTO Recipe
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (recipe_name, serving_size, cooking_time, tag, 
                        ingredient_name, amount,
                        nutrition_name, energy,
                        steps_taken))
        
        Model.connection.commit()

    def get_recipe_names():
        """
​	    This function returns a list of recipe names in the Recipe database 
​	    @parameters: none
​	    @return: a tuple contains only recipes’ name in the database 
​	    """
        # return list of Recipe Names in Recipe db
        Model.cursor.execute(''' SELECT recipe_name FROM Recipe''')
        data = Model.cursor.fetchall()
        Model.connection.commit() 

        return data 

    def get_recipe(name):
        """
    ​	This function returns a recipe object whose name is the recipe name 
    ​	Get the recipe data based on its name, including size of serving, cooking time, ingredient with the amount, and the nutrition with its energy.
    ​	@parameters: name(String): the name of the recipe
    ​	@return: a tuple of data contains the information of serving_size , cooking_time , tag, 	ingredient_name, amount , nutrition_name, energy, steps_taken
    ​	"""
        # return Recipe object whose name is name
        Model.cursor.execute(''' SELECT * FROM Recipe 
                                WHERE recipe_name = (?) ''', (name,))
        data = Model.cursor.fetchone()
        Model.connection.commit()
        return data

 
    def set_mealplan(period, # the period of the plan
                free_time_to_cook, 
                nutritious_restriction, 
                recipes_list,  
                precooked_meals, 
                fixed_meals): 

        # get recipe_list and its cooking time 
        Model.cursor.execute('''SELECT recipe_name, cooking_time  
                                FROM Recipe''') 
        food =  Model.cursor.fetchall()

        # update nutritous_retriction in database UserDefinedMeal 
        Model.cursor.execute(''' UPDATE retrictious_restriction r 
                    SET r.retrictious_restriction = ? 
                ''', nutritious_restriction) 

        # get nutritous_retriction 
        Model.cursor.execute('''SELECT nutritous_retriction FROM UserDefinedMeal''') 
        nutritious_restriction = Model.cursor.fetchone() #str type
        json.loads(nutritious_restriction) # convert to list  

        meal_plan = [] 
        meal_plan += fixed_meals + precooked_meals 
        for nutrient in nutritious_restriction:
            nutritious_restriction[nutrient] -= fixed_meals.nutrient 

        while not nutritious_restriction.isEmpty(): 
            for row in random.choice(food):  
                for recipe, time_cooking in row:  
                    if time_cooking < free_time_to_cook:  
                        meal_plan.append(recipe)             
        return meal_plan 

    def get_mealplan(self, period):
        pass