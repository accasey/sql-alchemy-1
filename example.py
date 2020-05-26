import sqlalchemy as db
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/sqlalchemy')
print(engine.table_names())
connection = engine.connect()
results = engine.execute('SELECT * FROM posts LIMIT 10')
print('results type', type(results))

first_results: object = results.fetchone()
print('first_results', type(first_results))
print(first_results.items())
print(results.fetchmany(2))
print(results.fetchall())

# print(results.column)

query = 'SELECT *  FROM posts'
posts_df = pd.read_sql_query(query, engine)
# print(posts_df)
# print(posts_df.columns)
# print(posts_df.dtypes)
# print(posts_df.head())

print('-----------------------------------------------------------')
print(posts_df[['ViewCount', 'AnswerCount']].max())
print(posts_df[['ViewCount', 'AnswerCount']].min())
print(posts_df[['ViewCount', 'AnswerCount']].sum())
print('-----------------------------------------------------------')
print(posts_df[['ViewCount', 'AnswerCount']].describe())
print('-----------------------------------------------------------')
x = posts_df['AnswerCount']
y = posts_df['ViewCount']
colors = np.random.rand(25488)
plt.scatter(x, y, c=colors)
plt.title('Posts: Views vs. Answers')
plt.xlabel('Answers')
plt.ylabel('Views')
plt.show()
