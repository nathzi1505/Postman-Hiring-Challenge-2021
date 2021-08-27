import sqlalchemy as db

class PublicApiDatabaseHandler():
    
    def __init__(self, database_uri, drop_tables=True):
        self.engine = db.create_engine(database_uri)
        self.metadata = db.MetaData()
        self.connection = self.engine.connect()
        
        try:
            self.category_table = db.Table('category', self.metadata, autoload=True, autoload_with=self.engine)
            self.api_table = db.Table('api', self.metadata, autoload=True, autoload_with=self.engine)

            if drop_tables:
                self.__drop_tables()
            
            self.metadata.clear()
            self.__create_tables()       
        except:
            self.__create_tables()           
        
    def __drop_tables(self):        
        self.api_table.drop(self.engine)
        self.category_table.drop(self.engine)
        
    def __create_tables(self):        
        self.category_table = db.Table('category', self.metadata,                           
                  db.Column('category_id', db.Integer(), primary_key=True),
                  db.Column('category_name', db.String(255)),        
                )

        self.api_table = db.Table('api', self.metadata,                           
                      db.Column('api_id', db.Integer(), primary_key=True),
                      db.Column('api_name', db.Text(), nullable=False),
                      db.Column('api_description', db.Text()),     
                      db.Column('auth', db.String(255)),
                      db.Column('https', db.Boolean(), nullable=False),                           
                      db.Column('cors', db.String(16), nullable=False),
                      db.Column('link', db.Text(), nullable=False),
                      db.Column('category_id', db.Integer(), db.ForeignKey("category.category_id", ondelete="CASCADE"), 
                                nullable=False),           
                    )

        self.metadata.create_all(self.engine)
        
    
    def populate_categories(self, category_list):
        category_value_list =  [{"category_name": x} for x in category_list]
        query = db.insert(self.category_table)
        ResultProxy = self.connection.execute(query, category_value_list)

    def populate_apis_for_category(self, category, api_list):
        query = db.select([self.category_table.columns.category_id]).where(self.category_table.columns.category_name == category)
        category_id = self.connection.execute(query).scalar()
        
        for row in api_list: 
            api_name, api_description, auth, https, cors, link, _ = row.values()

            cors = cors.capitalize()
            api_name = api_name.capitalize()
            api_description = api_description.capitalize()

            if len(auth) == 0: auth = None
            if len(api_description) == 0: api_description = None    

            db_row = {
                "api_name": api_name,
                "api_description": api_description,
                "auth": auth,
                "https": https,
                "cors": cors,
                "link": link,
                "category_id": category_id
            }

            query = db.insert(self.api_table)
            ResultProxy = self.connection.execute(query, db_row)
