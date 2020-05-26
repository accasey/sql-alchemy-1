import sqlalchemy as db
import pandas as pd
import datetime

engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/test_mysql_sa')
connection = engine.connect()

# print(datetime.datetime.now())
with open('tags.csv', 'r') as file:
    tags_df = pd.read_csv(file)
# print(datetime.datetime.now())
# print(tags_df.head())

tags_df.to_sql('tags', con=engine)
# This created the table, inserted the data, and then did the commit
