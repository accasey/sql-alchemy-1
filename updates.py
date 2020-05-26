import sqlalchemy as db
# needed for Update
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/test_mysql_sa')
connection = engine.connect()

# Using SQL
result = engine.execute('select * from posts where id = 1').fetchone()
print('Type:', type(result))
print('Result:', result)
print('--------------------------------------')
result = engine.execute('select viewcount from posts where id = 1').fetchone()
print('Type:', type(result))
print('Result:', result)
print('--------------------------------------')
result = engine.execute('update posts set viewcount = 0 where id = 1')
print('Type:', type(result))
print('Result:', result)
print('--------------------------------------')
result = engine.execute('select viewcount from posts where id = 1').fetchone()
print('Type:', type(result))
print('Result:', result)
print('--------------------------------------')

# Using Update
session = sessionmaker()
session.configure(bind=engine)
my_session = session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(50))


class Post(Base):
    __tablename__ = 'posts'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    Title = db.Column(db.String(255), nullable=False)
    ViewCount = db.Column(db.Integer(), default=1000)
    Question = db.Column(db.Boolean(), default=True)
    OwnerUserId = db.Column(db.Integer(), db.schema.ForeignKey('user.Id'), nullable=False)
    User = relationship('User', backref='post')


stmt = db.update(Post).where(Post.Id == 1).values(ViewCount=1)
print('Stmt Type:', type(stmt))
print('Stmt:', stmt)  # This actually prints the SQL statement
result = connection.execute(stmt)  # this seems to execute a commit as well
print('Result Type:', type(result))
print('Result:', result)
post_query = my_session.query(Post).filter(Post.Id == 1)
print('Type post_query', type(post_query))
print('Post query:', post_query)  # This actually prints the SQL statement
print('Post query result:', type(post_query.one()), post_query.one().Id, post_query.one().Title,
      post_query.one().ViewCount)

# Updating multiple records
# stmt = db.update(Post).values(ViewCount = Post.ViewCount + 50)
# result = connection.execute(stmt)
# You can also modify the object directly, once populated from the database
my_post = my_session.query(Post).filter(Post.Id == 1).one()
print(my_post.Title)
my_post.Title = 'Modified the question'
print('Dirty?:', my_session.dirty) # This returns an IdentitySet with a list of Post objects
my_session.commit()

# Use a function, this is the equivalent of select avg(viewcount) from posts
avg_views = db.select([db.func.avg(Post.ViewCount).label('AverageViews')])
# This does not work..
stmt = db.update(Post).values(ViewCount=avg_views)
# print('Type:', type(avg_views), str(avg_views))
result = connection.execute(stmt)