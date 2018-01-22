import datetime
import os
import re
import traceback
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongo_helper import *

try:
	is_test = os.environ['test']
except:
	is_test = None

mongo_client = MongoClient('mongodb://mongodb:27017')
if (is_test is not None):
	db = mongo_client.hellofresh_test_db
else:
	db = mongo_client.hellofresh_db

recipes_collection = db.recipes
recipe_ratings = db.recipe_ratings

def insert(recipe_attrs):
	if validate_input(recipe_attrs):
		recipe_attrs = clean_input(recipe_attrs)
		recipe_attrs['created_at'] = datetime.datetime.now()
		recipes_collection.insert_one(recipe_attrs)
		return True
	else:
		print ("Input validation failed.. Please check your input.")
		return False


def list():
	return [recipe for recipe in recipes_collection.find()]


def get_recipe(id):
	try:
		result = [recipe for recipe in recipes_collection.find({'_id': ObjectId(id)})]
		if len(result) > 0:
			return result[0]
		else:
			return None
	except:
		print (traceback.format_exc())
		return None


def search(search_attrs):
	search_attrs = clean_search_input(search_attrs)
	query_params = []
	if "prep_time" in search_attrs:
		query_params.append({ 'prep_time' : {'$lte': search_attrs["prep_time"]}})
	if "difficulty" in search_attrs:
		query_params.append({ 'difficulty' : {'$lte': search_attrs["difficulty"]}})
	if "vegetarian" in search_attrs:
		query_params.append({ 'vegetarian' : {'$in': search_attrs["vegetarian"]}})
	if "name" in search_attrs:
		regex_string = '.*' + search_attrs["name"] + '.*'
		regex = re.compile(regex_string)
		query_params.append({ 'name' : {'$regex': regex}})


	if 'rating' in search_attrs:
		rating = search_attrs.pop('rating')
	else:
		rating = None


	if (len(query_params) > 0):
		results = recipes_collection.find({
			'$and': query_params
		})
	else:
		results = recipes_collection.find()

	results = [i for i in results]
	objectid_list = [i['_id'] for i in results]

	if rating is not None:
		print(objectid_list)
		recipes_with_ratings = recipes_collection.find({
			'$and': [
				{'recipe_id' : {'$in': objectid_list}},
				{'rating' : {'$gte': rating}}
			]
		})
		recipes_with_ratings = [i['recipe_id'] for i in recipes_with_ratings]
		filtered_results = [i for i in results if i['_id'] in recipes_with_ratings]
		return filtered_results
	else:
		return results


## {"rating": 5}
def rate_recipe(id, recipe_rating_attrs):
	if validate_rating_input(recipe_rating_attrs):
		if(get_recipe(id) is not None):
			recipe_ratings.insert_one({
				"rating": recipe_rating_attrs['rating'], 
				"recipe_id": ObjectId(id), 
				"created_at": datetime.datetime.now()
			})
			return True
		else:
			print("Recipe with id : " + str(id) + " doesn't exist..")
			return False
	else:
		print("Verify the input.")
		return False


def update(id, recipe_attrs):
	if validate_input(recipe_attrs, True):
		recipe_attrs = clean_input(recipe_attrs)
		recipes_collection.update({'_id': ObjectId(id)}, {"$set": recipe_attrs}, upsert=False)
		return True
	else:
		print ("Input validation failed.. Please check your input.")
		return False


def delete(id):
	result = recipes_collection.delete_one({'_id': ObjectId(id)})
	print(result)
	return True
