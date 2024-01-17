import datetime
from pymongoose.mongo_types import Types, Schema

class FileInfo (Schema):
	schema_name = "files.info"

	def __init__ (self, **kwargs):
		self.schema = {
			"file": {
				"type": Types.ObjectId,
				"ref": "files",
				"default": None
			},
			"filename": {
				"type": Types.String,
				"required": True
			},
			"name": {
				"type": Types.String,
				"required": True
			},
			"phone": {
				"type": Types.String,
				"default": None
			},
			"md5": {
				"type": Types.String,
				"default": None
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Depot: {self.id}"