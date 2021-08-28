PublicAPIs List Crawler
--------------------------------------------------------

# Installation
--------------------------------
$ git clone https://github.com/nathzi1505/Postman-Hiring-Challenge-2021
$ docker-compose up --build --force-recreate

## MySQL with Docker
-----------
$ docker ps # - Extract container id for mysql
$ docker exec -it $CONTAINER_ID /bin/bash
$ mysql -proot -uroot
> USE postman;
...

# Tables
--------------------------------
Two tables - "api" and "category"

## Number of Rows
-----------
api        640
category    45

## Database Schema
-----------
Table: category
+---------------+--------------+------+-----+---------+------------------+
| Field         | Type         | Null | Key | Default | Extra            |
+---------------+--------------+------+-----+---------+------------------+
| category_id   | int          | NO   | PRI | NULL    | auto_increment   |
| category_name | varchar(255) | YES  |     | NULL    |                  |
+---------------+--------------+------+-----+---------+------------------+

Table: api
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| api_id          | int          | NO   | PRI | NULL    | auto_increment |
| api_name        | text         | NO   |     | NULL    |                |
| api_description | text         | YES  |     | NULL    |                |
| auth            | varchar(255) | YES  |     | NULL    |                |
| https           | tinyint(1)   | NO   |     | NULL    |                |
| cors            | varchar(16)  | NO   |     | NULL    |                |
| link            | text         | NO   |     | NULL    |                |
| category_id     | int          | NO   | MUL | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+


## Create Databases
-----------
Version  : SQLAlchemy
Source   : public_api_database_handler.py
...
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
...

# Points to Achieve
--------------------------------
[X] Follow OOPS principles.
        - Developed classes "PublicApi" and "PublicApiDatabaseHandler" to efficiently handle the functions of the crawler.

[X] Provide support for handling authentication requirements & token expiration of server
        - On "403 Forbidden", automatic regeneration of token is performed.

[X] Provide support for pagination to get all data
        - Looping through different pages until a zero length list is returned.

[X] Develop work around for rate limited server
        - Sleep timeouts are enforced when "429 Too Many Requests" is returned from the server.

[X] Crawl all API entries for all categories and store it in a database
        - All API entries have been crawled and stored in a MySQL database.
        - No. of total entries in "api" table : 640

# Not done from Points to Achieve
--------------------------------
None

# Future Improvements
--------------------------------
[X] Addition of logging and volume mounts to efficiently monitor api requests.
[X] Containerization for easy deployment.
[X] Extensive documentation of scripts.
[ ] Usage of a cloud database to host the data.
[ ] Added unit testing following good production grade software development practices.
[ ] Development of a CircleCI/TravisCI build based on a subset of data upon every push to GitHub. 
