from pymongo import MongoClient
from bson.objectid import ObjectId
import traceback

mongo_client = MongoClient('localhost:27017')
db = mongo_client.hellofresh_db
recipes_collection = db.recipes
NAME_MIN_LENGTH = 3


def insert(recipe_attrs):
	if validate_input(recipe_attrs):
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

def update(id, recipe_attrs):
	if validate_input(recipe_attrs):
		recipes_collection.update({'_id': id}, {"$set": recipe_attrs}, upsert=False)
		return True
	else:
		print ("Input validation failed.. Please check your input.")
		return False


def delete(id):
	result = recipes_collection.delete_one({'_id': ObjectId(id)})
	print(result)
	return True


def rate(id, rating):
	recipes_collection.update({'_id': id}, {"$set": {"rating": rating}})
	return True


def validate_input(recipe_attrs):
	try:
		name, prep_time, difficulty, vegetarian = unwrap_variables(recipe_attrs)

		type_validation = validate_class(name, str) and validate_class(prep_time, int) \
			and validate_class(difficulty, int) and validate_class(vegetarian, bool)

		if type_validation:
			if difficulty_value_validation(difficulty) and name_length_validation(name):
				return True

		return False
	except:
		print ("Exception while validating input.. Please check input.")
		return False

def unwrap_variables(recipe_attrs):
	try:
		name = recipe_attrs.get('name')
		prep_time = recipe_attrs.get('prep_time')
		difficulty = recipe_attrs.get('difficulty')
		vegetarian = recipe_attrs.get('vegetarian')
		return name, prep_time, difficulty, vegetarian
	except KeyError:
		print (traceback.format_exc())
		return None, None, None, None

def validate_class(obj, klass):
	if type(obj) == klass:
		return True
	else:
		return False


def difficulty_value_validation(val):
	if val in [1,2,3]:
		return True
	else:
		return False

def name_length_validation(name):
	return (len(name) > NAME_MIN_LENGTH)
