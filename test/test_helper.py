
def clean_db(recipes_collection, recipe_ratings):
	recipes_collection.remove({})
	recipe_ratings.remove({})
