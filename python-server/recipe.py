import json
import pymongo

# Schema:
    # - Unique ID
    # - Name
    # - Prep time
    # - Difficulty (1-3)
    # - Vegetarian (boolean)


class Recipe:
	def __init__(recipe_attrs):
		try:
			self.name = recipe_attrs.get('name')
			self.prep_time = recipe_attrs.get('prep_time')
			self.difficulty = recipe_attrs.get('difficulty')
			self.vegetarian = recipe_attrs.get('vegetarian')
		except KeyError:
			print "Error initializing the recipe.." 
		
	
