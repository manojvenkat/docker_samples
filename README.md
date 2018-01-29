Stack choice : 
	- Python 3.6
	- MongoDB
	- Docker

Packages Used : 
	- pymongo for connecting/querying to mongodb
	- http.server for handling http request/response
	- unittest for writing unit & functional tests

Startup : 
	- Type "docker-compose up" to start the mongodb and the python server.

Testing :
	Unit testing:
		- Go to 'test' folder and run "python3 mongo_test.py"
	Functional testing: 
		- You need to run a test server first. Go to "python_server" folder, type "python3 test_server.py"
		- Then go to "test" folder and run "python3 integration_test.py"

Code formatting:
	- Used flake8 to format the code. Some modules are still pending to code formatting.
	- But will be flake8 standards to format the code.


API Details :

	Following APIs are implemented : 
		1. Create API
		2. List API
		3. Rating API
		4. Delete API
		5. Get API
		6. Update API
		7. Search API

	All except for "Search API" are implemented according to the problem statement and adheres to REST-fulness.


Search API details:

	- Search API is implemented as POST API. 
	- URL : "http://localhost:8080/search/recipes"
	- Takes a json payload as the search parameters
	- JSON payload format : 
		{
			'name': "XYZ",    			---> "Look for a substring match i.e. search for recipe name with 'xyz'"
			'difficulty': 3,  			---> "Look for recipes that are lesser or equally difficult than 3"
			'prep_time': 120, 			---> "Look for recipes that have prep_time lesser than 120 mins"
			'vegetarian': [true] 		---> "Look for recipes that are vegetarian."
			'rating': 3					---> "Look for recipes that are rated above 3."
		}
	- None of the fields are compulsory. If there are no valid parameters, 
	  then the whole list of recipes will be returned.
	