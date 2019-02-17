# Assignment 3

## Twitter data

### Question 1
How many Twitter users are in the database?

```python
users = db.tweets.distinct("user")
```

```
Number of users:  659775
```

### Question 2
Which Twitter users link the most to other Twitter users? (Provide the top ten.)

```python
pipeline = [
    {"$match": {"text": {"$regex": "@\\w*"}}},
    {"$group": {"_id": "$user", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("user", -1)])},
    {"$limit": 10}
]
result = db.tweets.aggregate(pipeline)
```


```
{'_id': 'lost_dog', 'count': 549}
{'_id': 'tweetpet', 'count': 310}
{'_id': 'VioletsCRUK', 'count': 251}
{'_id': 'what_bugs_u', 'count': 246}
{'_id': 'tsarnick', 'count': 245}
{'_id': 'SallytheShizzle', 'count': 229}
{'_id': 'mcraddictal', 'count': 217}
{'_id': 'Karen230683', 'count': 216}
{'_id': 'keza34', 'count': 211}
{'_id': 'TraceyHewins', 'count': 202}
```

### Question 3
Who is are the most mentioned Twitter users? (Provide the top five.)

```python
pipeline = [
    {"$match": {"text": {"$regex": "@\\w*"}}},
    {"$group": {
        "_id": {"$substrCP": 
            ["$text", 
                {"$indexOfCP": ["$text", "@"]}, 
                {"$indexOfCP": ["$text", " "]}
            ]},
        "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("user", -1)])},
    {"$limit": 5}
]
result = db.tweets.aggregate(pipeline)
```


```
{'_id': '@', 'count': 6268}
{'_id': '@mileycyrus', 'count': 3771}
{'_id': '@tommcfly', 'count': 3616}
{'_id': '@ddlovato', 'count': 2926}
{'_id': '@DavidArchie', 'count': 1089}
```

### Question 4
Who are the most active Twitter users (top ten)?

```python
pipeline = [
    {"$group": {"_id": "$user", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("user", -1)])},
    {"$limit": 10}
]
result = db.tweets.aggregate(pipeline)
```


```
{'_id': 'lost_dog', 'count': 549}
{'_id': 'webwoke', 'count': 345}
{'_id': 'tweetpet', 'count': 310}
{'_id': 'SallytheShizzle', 'count': 281}
{'_id': 'VioletsCRUK', 'count': 279}
{'_id': 'mcraddictal', 'count': 276}
{'_id': 'tsarnick', 'count': 248}
{'_id': 'what_bugs_u', 'count': 246}
{'_id': 'Karen230683', 'count': 238}
{'_id': 'DarkPiano', 'count': 236}
```

### Question 5
Who are the five most grumpy (most negative tweets) and the most happy (most positive tweets)?

```python
pipeline = [
    {"$match": {"polarity": "4"}}, # 4 is positive, 0 is negative
    {"$group": {"_id": "$user", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("user", -1)])},
    {"$limit": 5}
]
result_happy = db.tweets.aggregate(pipeline)
```


```
5 most happy:
{'_id': 'what_bugs_u', 'count': 246}
{'_id': 'DarkPiano', 'count': 231}
{'_id': 'VioletsCRUK', 'count': 218}
{'_id': 'tsarnick', 'count': 212}
{'_id': 'keza34', 'count': 211}
5 most grupmy:
{'_id': 'lost_dog', 'count': 549}
{'_id': 'tweetpet', 'count': 310}
{'_id': 'webwoke', 'count': 264}
{'_id': 'mcraddictal', 'count': 210}
{'_id': 'wowlew', 'count': 210}
```

## Modeling

| Model | Atomicity | Sharding | Indexes | Large Number of Collections | Collection Contains Large Number of Small Documents |
|:-----|:---------:|:--------:|:-------:|:---------------------------:|:---------------------------------------------------:|
| Arrays of Ancestors | X |  | X | X |  |
| Materialized paths |  | X |  | X | X |
| Nested sets | X | X | X |  |  |

### Arguments

- **Arrays of Ancestors**:
  - Atomicirty: You only write to one document
  - Indexes: It is posible to index 
  - Large Number of Collections: Each document must refer to it's ancestors, so you can get a large collection 
- **Materialized paths**:
  - Sharding: TODO
  - Large Number of Collections: TODO
  - Collection Contains Large Number of Small Documents: TODO
- **Nested sets**:
  - Atomicity: TODO
  - Sharding: TODO
  - Indexes: TODO
