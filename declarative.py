'''
This is the 'typically' used system.
It is provided by the SQLAlchemy ORM
You define classes which are mapped to relational database tables.
They are a series of extensions on top of the mapper construct.
 - mapping.py
'''
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import Table, MetaData, Column, Integer, String, func
from tags import Tags
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/sqlalchemy')
# You can also add the echo parameter here to see the sql being generated:
# engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/sqlalchemy', echo=True)
print(engine.table_names())
# connection = engine.connect()

# The session establishes and maintains conversations between the program
# and the database. It is an entry point for queries, or interactions with the
# database
session = sessionmaker()
session.configure(bind=engine)

my_session = session()
# This will generate a list of Tags objects
list_of_tags = my_session.query(Tags).all()
print(len(list_of_tags))
# Generates a single Tags object
first_tag = my_session.query(Tags).first()
# print(type(first_tag))
# print(first_tag.Id)
# print(first_tag.Count)
# print(first_tag.ExcerptPostId)
# print(first_tag.TagName)
# print(first_tag.WikiPostId)

# This returns class 'sqlalchemy.util._collections.result
# But it seems like a tuple
# And without the 'type' it returns
#     (1, 'definitions')
first_tag_flds = my_session.query(Tags.Id, Tags.TagName).first()
# print(type(first_tag_flds))
# print(first_tag_flds)


# Now use the 'declarative api'
Base = declarative_base()


class Posts(Base):
    '''The fields defined here do not need to be all the fields'''
    __tablename__ = 'posts'
    Id = db.Column(db.Integer(), primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ViewCount = db.Column(db.Integer(), default=1000)
    PostTypeId = db.Column(db.Integer(), default=True)
    OwnerUserId = db.Column(db.Integer())
    # Define 'derived' columns
    Test = 'Test'

    # not sure that this was necessary, he was using the repl
    # maybe that had something to do with it..
    __table_args__ = {'extend_existing': True}
    AnswerCount = db.Column(db.Integer)
    ParentId = db.Column(db.Integer)
    Score = db.Column(db.Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__} Id: {self.Id} Title: {self.Title} \
ViewCount: {self.ViewCount} PostTypeId: {self.PostTypeId} \
OwnerUserId: {self.OwnerUserId} Test: {self.Test}>"


class Users(Base):
    '''The class must inherit from declarative_base, and specify __tablename__ '''
    __tablename__ = 'users'
    # declare columns with type
    Id = Column(db.Integer, primary_key=True)
    Reputation = db.Column(db.Integer)
    CreationDate = db.Column(db.DateTime)
    DisplayName = db.Column(db.String(255))
    LastAccessDate = db.Column(db.DateTime)
    # WebsiteUrl = db.column(db.String(255))
    WebsiteUrl = Column(db.String(255))
    Location = db.Column(db.String(4096))
    AboutMe = db.Column(db.String(4096))
    Views = db.Column(db.Integer)
    UpVotes = db.Column(db.Integer)
    DownVotes = db.Column(db.Integer)
    AccountId = db.Column(db.Integer)
    ProfileImageUrl = db.Column(db.String(255))

    def __repr__(self):
        return f'<{self.__class__.__name__} Id: {self.Id} - Name: {self.DisplayName}>'


# This is an object of type __main__.Users
users_first = my_session.query(Users).first()
print(users_first.WebsiteUrl)

# You could also iterate over the results
# But this table has 46,189 rows :/
# for each_user in my_session.query(Users):
#     print(each_user)
# You can also load the results into a pandas data frame


# <class 'sqlalchemy.orm.query.Query'>
the_query = my_session.query(Users)
# print(type(the_query))

# This shows the query being generated against the database
# print(the_query)

# You can use 'filter_by', but restricted to one table
# print(my_session.query(Users).filter_by(DisplayName='Community').all())
# With 'filter', you can use multiple tables
# print(my_session.query(Users).filter(Users.DisplayName == 'Community').all())

# Using the 'like' operator clause/filter
# This returns the __repr__ result
# print(my_session.query(Users).filter(Users.DisplayName.like('%Comm%')).all())
# This returns a single column
# print(my_session.query(Users.DisplayName).filter(Users.DisplayName.like('%Comm%')).all())
# This returns the two columns
# print(my_session.query(Users.DisplayName, Users.Views).filter(Users.DisplayName.like('%Comm%')).all())

# You can also use 'contains'
# print(my_session.query(Users.DisplayName).filter(Users.DisplayName.contains('comm')).all())

# This is the equivalent of 'select sum(count) from tags;'
# print(my_session.query(func.sum(Tags.Count)).scalar())
# Use scalar to return a single element

# Create a derived column and give it a label, then limit it to 5 rows.
print(my_session.query(Users.DisplayName,
                       db.cast((Users.UpVotes - Users.DownVotes), db.Numeric(12, 2)).label('vote_difference'),
                       Users.UpVotes,
                       Users.DownVotes)
      .limit(5).all())
# You can also add an order by before the limit (default is 'asc')
print(my_session.query(Users.DisplayName,
                       db.cast((Users.UpVotes - Users.DownVotes), db.Numeric(12, 2)).label('vote_difference'),
                       Users.UpVotes,
                       Users.DownVotes)
      # .order_by('vote_difference')
      .order_by(db.desc('vote_difference'))
      .limit(5)
      .all())

# Conjunctions, and_, or_, not_
# 'and_' is the default
print(my_session.query(Users)
      .filter(db.or_(Users.DisplayName == 'Community', Users.DownVotes.between(300, 600)))
      .all())

# Joining data, two ways
# 1. Implicit join
print(my_session.query(Users, Posts).filter(Users.Id == Posts.OwnerUserId).first())

# 2. Explicit join
print(my_session.query(Users, Posts).join(Posts, Users.Id == Posts.OwnerUserId).first())

print('-------------------- Hierarchical -----------------')
Questions = aliased(Posts)
print(my_session.query(Posts.Id, Questions.Id, Posts.ViewCount, Posts.Score, Questions.Score)
      .filter(Posts.Id == Questions.ParentId)
      .order_by(db.desc(Posts.ViewCount))
      .limit(10)
      .all())