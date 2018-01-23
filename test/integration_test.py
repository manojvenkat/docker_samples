import sys
sys.path.append('../python_server')
import unittest
import json
import types
import os
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
from test_helper import *
from security_keys import *

os.environ["test"] = "True"
test_client = mongo_client = MongoClient('mongodb://mongodb:27017')
db = mongo_client.hellofresh_test_db
recipes_collection = db.recipes
recipe_ratings = db.recipe_ratings


## Run the test server - "python3 ../python_server/test_server.py" ##

class IntegrationTestModule(unittest.TestCase):

	def test_create_api(self, clean=True):
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		headers = {'content-type': 'application/json', 'secret_key': SECRET_KEY}
		response = requests.post("http://localhost:8080/recipes", \
			data=json.dumps(recipe_attrs), headers=headers)
		self.assertEqual(response.status_code, 200)
		if(clean):
			clean_db(recipes_collection, recipe_ratings)


	def test_list_api(self, clean=True):
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		recipe_attrs_1 = {"name": "Chicken Butter Masala", \
			"prep_time": 100, "difficulty": 3, "vegetarian": False}
		headers = {'content-type': 'application/json', 'secret_key': SECRET_KEY}
		create_response = requests.post("http://localhost:8080/recipes", \
			data=json.dumps(recipe_attrs), headers=headers)
		create_response = requests.post("http://localhost:8080/recipes", \
			data=json.dumps(recipe_attrs_1), headers=headers)
		self.assertEqual(create_response.status_code, 200)

		list_response = requests.get("http://localhost:8080/recipes")
		data = json.loads(list_response.content)
		recipes = data['data']

		self.assertEqual(len(recipes), 2)

		if(clean):
			clean_db(recipes_collection, recipe_ratings)


	def test_rating_api(self, clean=True):
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		headers = {'content-type': 'application/json', 'secret_key': SECRET_KEY}
		create_response = requests.post("http://localhost:8080/recipes", \
			data=json.dumps(recipe_attrs), headers=headers)
		self.assertEqual(create_response.status_code, 200)
		list_response = requests.get("http://localhost:8080/recipes")
		data = json.loads(list_response.content)
		recipe_id = data['data'][0]['_id']['$oid']

		rating_url = "http://localhost:8080/recipes/" + recipe_id + "/rating"
		requests.post(rating_url, data=json.dumps({'rating': 4}), headers=headers)
		requests.post(rating_url, data=json.dumps({'rating': 3}), headers=headers)
		ratings = recipe_ratings.find({'recipe_id' : {'$in': [ObjectId(recipe_id)]}})
		ratings = set([i['rating'] for i in ratings])
		self.assertEqual(ratings, set([3,4]))

		if(clean):
			clean_db(recipes_collection, recipe_ratings)
	

	def test_search_api(self, clean=True):
		search_url = 'http://localhost:8080/search/recipes'

		self.test_list_api(clean=False)
		self.test_rating_api(clean=False)

		search_params = {'rating': 3, 'vegetarian': [True]}
		headers = {'content-type': 'application/json'}
		response = requests.post(search_url, data=json.dumps(search_params),headers=headers)
		data = json.loads(response.content)
		recipe = data['data'][0]
		self.assertEqual(recipe['name'], 'Chicken Tikka Masala')

		if(clean):
			clean_db(recipes_collection, recipe_ratings)


if __name__ == '__main__':
	unittest.main()