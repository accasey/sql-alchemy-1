'''
Classical Mapping
'''
import sqlalchemy as db
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper
from tags import Tags

engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/sqlalchemy')
print(engine.table_names())
connection = engine.connect()

metadata = MetaData()

tags = Table('Tags', metadata,
             Column('Id', Integer, primary_key=True),
             Column('Count', Integer),
             Column('ExcerptPostId', Integer),
             Column('TagName', String(255)),
             Column('WikiPostId', Integer))


tags_mapper = mapper(Tags, tags)

larger_tags = tags.select(Tags.Count > 1000)
print(type(larger_tags))

result = engine.execute(larger_tags).fetchall()
print(type(result))
print('------------------')
print(result)