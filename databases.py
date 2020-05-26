import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


# Create a database
def create_database():
    engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306')
    connection = engine.connect()
    engine.execute('create database test_mysql_sa;')
    # You can see this is empty by running 'show tables;' in the client


engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/test_mysql_sa')
metadata = db.MetaData()  # <- a container object

# posts = db.Table('posts', metadata,
#                  db.Column('Id', db.Integer),
#                  db.Column('Title', db.String(255)),
#                  db.Column('ViewCount', db.Integer),
#                  db.Column('IsQuestion', db.Boolean()))

# metadata.create_all(engine)
# print(posts)
# print(list(posts.c))
# print(dir(posts))

# Even with the default values being set here, the values from the manual inserts
# in the sql client (i.e. not Python) are null;
# posts_two = db.Table('posts_two', metadata,
#                      db.Column('Id', db.Integer(), primary_key=True, unique=True),
#                      db.Column('Title', db.String(255), nullable=False),
#                      db.Column('ViewCount', db.Integer(), default=1000),
#                      db.Column('Question', db.Boolean(), default=True))
# posts_two.create(engine)

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

Base.metadata.create_all(engine)


connection = engine.connect()

users = db.Table('user', metadata, autoload=True, autoload_with=engine)
# <class 'sqlalchemy.sql.schema.Table'>
stmt = db.insert(users).values(Name='Andrew Casey')
# <class 'sqlalchemy.sql.dml.Insert'>
result = connection.execute(stmt)
# <class 'sqlalchemy.engine.result.ResultProxy'>
# You can also use result.rowcount


# insert using session
session = sessionmaker()
# <class 'sqlalchemy.orm.session.sessionmaker'>
session.configure(bind=engine)
my_session = session()
# <class 'sqlalchemy.orm.session.Session'>

Ebru = User(Name='Ebru')
Jack = User(Name='Jack')
my_session.add(Ebru)
my_session.add(Jack)
# print(my_session.new) <-- this gives the two objects below
# It is the two objects defined above in the IdentitySet
# IdentitySet([<__main__.User object at 0x000001C54F6731F0>, <__main__.User object at 0x000001C54F6C66D0>])
my_session.commit()

for each_user in my_session.query(User).all():
    print(each_user.Name)


posts = db.Table('posts', metadata, autoload=True, autoload_with=engine)
stmt = db.insert(posts)
values_list = [
    {
        'Title': 'Data Science Question',
        'OwnerUserId': 1
    },
    {
        'Title': 'Big Data Question',
        'OwnerUserId': 8
    }
]

result = connection.execute(stmt, values_list)

# You can also use an User object here instead of '1'
# The Question column has one_post = Post(Title='Sample question', OwnerUserId=1)
# one_answer = Post(Title='Sample answer', Question=False, OwnerUserId=1)
# # ViewCount was not included in either as it has its own default value
#
# # Pass an iterable object
# my_session.add_all([one_post, one_answer])
# my_session.commit()a default value of True
