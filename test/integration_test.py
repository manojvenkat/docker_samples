import unittest
import json
import types
import os
import sys
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId

sys.path.append('../python_server')
os.environ["test"] = "True"
test_client = mongo_client = MongoClient('mongodb://mongodb:27017')
db = mongo_client.hellofresh_test_db
recipes_collection = db.recipes
recipe_ratings = db.recipe_ratings


## Run the test server - "python3 ../python_server/test_server.py" ##

class IntegrationTestModule(unittest.TestCase):

	def test_create_api(self):
		recipe_attrs = {"name": "Chicken Tikka Masala", \
			"prep_time": 120, "difficulty": 3, "vegetarian": True}
		headers = {'content-type': 'application/json'}
		response = requests.post("http://localhost:8080/recipes", \
			data=json.dumps(recipe_attrs), headers=headers)
		self.assertEqual(response.status_code, 200)


	def test_list_api(self):
		pass


if __name__ == '__main__':
	unittest.main()