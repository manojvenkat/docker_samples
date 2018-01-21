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

	if ("rating" in search_attrs):
		if ((not isinstance(search_attrs['rating'], int)) \
			or (not (search_attrs['rating'] in range(1,6)))):
			search_attrs.pop('rating')

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
		(recipe_rating_attrs['rating'] in range(1,6))
