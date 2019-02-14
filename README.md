# Assignment 2/3 - Analysis of Twitter Data

## Twitter data

### Question 1
How many Twitter users are in the database?

```python
users = db.tweets.distinct("user")
```

We use the Mongo DB `distinct` function to get each user only once.

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

**TODO write description of pipeline**

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

**TODO write description of pipeline**

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

**TODO write description of pipeline**

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

**TODO write description of pipeline**

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


## Twitter Database

This program should be able to do the following:

1. Import data from a csv file into a mongo database
2. Tell how many Twitter users are in the database?
3. Tell which Twitter users link the most to other Twitter users? (Provide the top ten.)
4. Tell who is are the most mentioned Twitter users? (Provide the top five.)
5. Tell who are the most active Twitter users (top ten)?
6. Tell who are the five most grumpy (most negative tweets) and the most happy (most positive tweets)?

This program uses the Twitter dataset from Sentiment140

[Link to the source](http://help.sentiment140.com/for-students/)

## Requirements

This program uses Python3, to run it correctly you must have Python3. 

It uses one non standart library, `pymongo`. In a bash terminal you can type `pip3 list | grep -F pymongo` to check if you have it installed. If you dont have it, you can type `pip3 install --user pymongo` to install it. 

## How to run the program

This program uses the standart library `argparse`, so if you type `python3 run.py -h` you'll get help text for the program. Here you can see positional arguments and optional arguments. Options in squared brackets are optional. 

To run the program, you'll first need to initalize it. This is done by typing `python3 run.py -i <csv file path>`.

When the database have been initialized, type `python3 run.py -r q [1-5]` to run one of the questions. E.g. `python3 run.py -r q 1` runs the first question

