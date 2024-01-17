import traceback

from pymongo import MongoClient
from pymongoose.methods import set_schemas

from config import MONGO_URL
from models.file_info import FileInfo

db = None

def db_mongo_init ():
	global db

	result = False

	client = MongoClient (MONGO_URL)
	try:
		db = client.db

		db.command ("ping")

		schemas = {
			"files.info": FileInfo (empty=True).schema			
		}

		set_schemas (
			db, schemas,
			False
		)

		result = True

	except:
		traceback.print_exc ()

	return result
