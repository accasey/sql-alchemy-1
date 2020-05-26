from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper


class Tags():
    def __init__(self, Count, ExcerptPostId, TagName, WikiPostId):
        self.Count = Count
        self.ExcerptPostId = ExcerptPostId
        self.TagName = TagName
        self.WikiPostId = WikiPostId


metadata = MetaData()

tags = Table('Tags', metadata,
             Column('Id', Integer, primary_key=True),
             Column('Count', Integer),
             Column('ExcerptPostId', Integer),
             Column('TagName', String(255)),
             Column('WikiPostId', Integer))

tags_mapper = mapper(Tags, tags)
