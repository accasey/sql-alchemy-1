# Inserts

## Insert using a Statement
```python
stmt = db.insert(users).values(Name='Andrew Casey')
result = connection.execute(stmt)
```

## Insert using a Session
```python
my_session = session()
Ebru = User(Name='Ebru')
Jack = User(Name='Jack')
my_session.add(Ebru)
my_session.add(Jack)
my_session.commit()
```

## Inserting multiple records using a Statement
```python
result = connection.execute(stmt, values_list)
```

## Insert multiple records using a Session
```python
one_post = Post(Title='Sample question', OwnerUserId=1)
one_answer = Post(Title='Sample answer', Question=False, OwnerUserId=1)
my_session.add_all([one_post, one_answer])
my_session.commit()
```