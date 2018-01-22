import unittest
import os
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

sys.path.append('../python_server')
os.environ["test"] = "True"
test_client = mongo_client = MongoClient('mongodb://mongodb:27017')
db = mongo_client.hellofresh_test_db
recipes_collection = db.recipes
recipe_ratings = db.recipe_ratings

import mongo


class MongoTestModule(unittest.TestCase):

	def test_create(self):
		print "** Running create test **"
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		result = mongo.insert(recipe_attrs)
		if(result):
			recipes = recipes_collection.find({})
			inserted_recipe = [recipe for recipe in recipes][0]
			inserted_recipe = {i: inserted_recipe[i] for i in recipe_attrs.keys()}
			self.assertEqual(inserted_recipe, recipe_attrs)
		else:
			print "Insertion unsuccessful.."
			assert False
		clean_db()


	def test_list(self):
		print "** Running List test **"
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		recipe_attrs_1 = {"name": "Butter Chicken Masala", \
			"prep_time": 100, "difficulty": 2, "vegetarian": False}

		result = mongo.insert(recipe_attrs)
		result_2 = mongo.insert(recipe_attrs)
		if(result and result_2):
			recipes = recipes_collection.find({})
			inserted_recipes = [recipe for recipe in recipes]
			self.assertEqual(len(inserted_recipes), 2)
		else:
			print "Insertion unsuccessful.."
			assert False
		clean_db()


	def test_get_recipe(self):
		print "** Testing Get recipe by ID **"
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		result = mongo.insert(recipe_attrs)
		if(result):
			recipes = recipes_collection.find({})
			inserted_recipe = [recipe for recipe in recipes][0]
		else:
			print "Insertion unsuccessful.."
			assert False
		clean_db()


def clean_db():
	recipes_collection.remove({})
	recipe_ratings.remove({})

if __name__ == "__main__":
	unittest.main()

