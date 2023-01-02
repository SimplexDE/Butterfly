from pymongo import MongoClient




class MongoDB:
	def __init__(self, db_name, collection_name):
		self.db_name = db_name
		self.collection_name = collection_name
		self.client = MongoClient("localhost", 27017)
		self.db = self.client[self.db_name]
		self.collection = self.db[self.collection_name]


	def insert_one(self, data: dict):
		return self.collection.insert_one(data)


	def insert_many(self, data: dict):
		return self.collection.insert_many(data)


	def find_one(self, query: dict):
		return self.collection.find_one(query)


	def find_many(self, query: dict):
		return self.collection.find(query)


	def update_one(self, query: dict, data: dict):
		return self.collection.update_one(query, data)


	def update_many(self, query: dict, data: dict):
		return self.collection.update_many(query, data)


	def delete_one(self, query: dict):
		return self.collection.delete_one(query)


	def delete_many(self, query: dict):
		return self.collection.delete_many(query)


	def drop_collection(self, collection_name):
		return self.db.drop_collection(collection_name)


	def drop_db(self, db_name):
		return self.client.drop_database(db_name)


	def show_collections(self):
		return self.db.list_collection_names()


	def show_databases(self):
		return self.client.list_database_names()


	def show_tables(self, db_name):
		return self.db[db_name].list_collection_names()


	def show_table_columns(self, db_name, table_name):
		return self.db[db_name][table_name].list_collection_names()


	def show_table_data(self, db_name, table_name):
		return self.db[db_name][table_name].find()


	def show_table_data_count(self, db_name, table_name):
		return self.db[db_name][table_name].count_documents({})


	def show_table_data_count_by_column(self, db_name, table_name, column_name):
		return self.db[db_name][table_name].count_documents({column_name: {'$exists': True}})


	def show_table_data_count_by_column_and_value(self, db_name, table_name, column_name, value):
		return self.db[db_name][table_name].count_documents({column_name: value})
