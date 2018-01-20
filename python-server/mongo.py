import datetime
import re
import traceback
from pymongo import MongoClient
from bson.objectid import ObjectId


mongo_client = MongoClient('localhost:27017')
db = mongo_client.hellofresh_db
recipes_collection = db.recipes
recipe_ratings = db.recipe_ratings
NAME_MIN_LENGTH = 3
VALID_KEYS_LIST = ['name', 'prep_time', 'difficulty', 'vegetarian']



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

	results = recipes_collection.find({
		'$and': query_params
	})

	results = [i for i in results]
	return results


## {"rating": 5}
def rate_recipe(id, recipe_rating_attrs):
	if validate_rating_input(recipe_rating_attrs):
		recipe_ratings.insert_one({
			"rating": recipe_rating_attrs['rating'], 
			"recipe_id": ObjectId(id), 
			"created_at": datetime.datetime.now()
		})
		return True
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


def validate_input(recipe_attrs, update=False):
	if (not update):
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
	else:
		## Need more validation here..
		update_hash = unwrap_variables_for_update(recipe_attrs)
		if len([i for i in update_hash.values() if i is not None]) > 0:
			return True


def clean_input(recipe_attrs):
	valid_keys = [i for i in recipe_attrs.keys() if i in VALID_KEYS_LIST]
	cleaned_recipe_attrs = {}
	for i in valid_keys:
		cleaned_recipe_attrs[i] =  recipe_attrs[i]
	return cleaned_recipe_attrs

def clean_search_input(search_attrs):
	if ("name" in search_attrs):
		if(not len(search_attrs["name"]) > 0):
			search_attrs.pop("name")

	if ("prep_time" in search_attrs):
		if(not isinstance(search_attrs["prep_time"], int)):
			search_attrs.pop("prep_time")

	if ("difficulty" in search_attrs):
		if((not isinstance(search_attrs["difficulty"], int)) \
			or (not difficulty_value_validation(search_attrs["difficulty"]))):
			search_attrs.pop("difficulty")

	if ("vegetarian" in search_attrs):
		if (not (len(search_attrs['vegetarian']) > 0)):
			search_attrs.pop("vegetarian")

	return search_attrs

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


def unwrap_variables_for_update(recipe_attrs):
	name = recipe_attrs.get('name', None)
	prep_time = recipe_attrs.get('prep_time', None)
	difficulty = recipe_attrs.get('difficulty', None)
	vegetarian = recipe_attrs.get('vegetarian', None)
	return {"name": name, "prep_time": prep_time, "difficulty": difficulty, "vegetarian": vegetarian}


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


def validate_rating_input(recipe_rating_attrs):
	return ('rating' in recipe_rating_attrs) and \
		(recipe_rating_attrs['rating'] in range(1,5))


