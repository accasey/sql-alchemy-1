import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine('mysql+mysqlconnector://admin:password@localhost:3306/test_mysql_sa')
connection = engine.connect()

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


# Delete from a Session by passing in the object
# works well for one at a time
def delete_1():
    print(my_session.query(Post.Id).all())
    first_post = my_session.query(Post).first()
    print(first_post.Id)
    my_session.delete(first_post)
    print(my_session.query(Post.Id).all())
    my_session.commit()


# Delete using a query as the source
def delete_2():
    obj = my_session.query(Post.Id).all()
    result = my_session.query(Post).filter(Post.Id > 2).delete()
    print(type(result), result)  # this is the rowcount
    my_session.commit()


# Deleting a table.
metadata = db.MetaData()
metadata.reflect(bind=engine)

print(metadata.tables.keys())
# dict_keys(['posts', 'user', 'tags'])
# print(metadata.tables.items()) type = dict_items <-- this also shows columns etc.
print(metadata.tables) #type = immutabledict and shows same as above two
# MetaData(bind=None)
posts_table = metadata.tables['posts']
# print(posts_table)
posts_table.drop(bind=engine)