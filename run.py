import re
import csv
import argparse
from bson import SON
from pprint import pprint
from pymongo import MongoClient

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--initialize", 
        help="Takes the csv file and creates a mongo db with the data", 
        action="store_true")
    parser.add_argument("csv_file",
        nargs="?",
        help="Path to the csv file")

    parser.add_argument("-r", "--run", 
        help="Run the main part of the program, needs to be initialized first",
        action="store_true")    
    parser.add_argument("question",
    nargs="?",
    type=int,
    help="Which question you want to run, 1-5")

    args = parser.parse_args()


    if args.initialize:
        initialize(args.csv_file) 

    if args.run:
        client = MongoClient()
        db = client['Tweets'] # change before push to github
        q = args.question
        if q == 1:
            twitter_users(db)
        elif q == 2:
            most_links(db)
        elif q == 3:
            most_mentions(db)
        elif q == 4:
            most_active(db)
        elif q == 5:
            most_polarity(db)
        else:
            print("Please input 1 to 5 in the positional argument 'question'")

def initialize(csv_file):
    print("Starting initializing...")
    client = MongoClient()
    db = client['Tweets']
    print("Reading csv file...")
    with open(csv_file, "r", encoding="ISO-8859-1") as csvfile:
        tweets = []
        fieldnames = ["polarity", "id", "date", "query", "user", "text"]
        reader = csv.DictReader(csvfile, fieldnames)
        for each in reader:
            row = {}
            for field in fieldnames:
                row[field] = each[field]
            
            tweets.append(row)
        
        print("Done reading csv file \nStarting mongo db import...")
        db.tweets.insert_many(tweets)
        print("Done importing to mongo db.")

    print("Done initializing.")


def twitter_users(db):
    print("1. How many Twitter users are in the database?")
    users = db.tweets.distinct("user")
    print("Number of users: ", len(users))


def most_links(db):
    print("2. Which Twitter users link the most to other Twitter users? (Provide the top ten.)")
    pipeline = [
        {"$match": {"text": {"$regex": "@\\w*"}}},
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("user", -1)])},
        {"$limit": 10}
    ]
    result = db.tweets.aggregate(pipeline)
    pp_all(result)


def most_mentions(db):
    print("3. Who is are the most mentioned Twitter users? (Provide the top five.)")
    pipeline = [
        {"$match": {"text": {"$regex": "@\\w*"}}},
        {"$group": {
            "_id": {"$substrCP": ["$text", {"$indexOfCP": ["$text", "@"]}, {"$indexOfCP": ["$text", " "]}]},
            "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("user", -1)])},
        {"$limit": 5}
    ]
    result = db.tweets.aggregate(pipeline)
    pp_all(result)
    
    """
    # Brute force
    rs = {}
    match = r"@(\\w*)"
    print(db.tweets.find_one({"text": {"$regex": "@"}}))
    for u in db.tweets.find({"text": {"$regex": "@"}}):
        m = re.match(match, u["text"])
        user = m.group(1)
        if user in rs.keys():
            rs[user] += 1
        else:
            rs[user] = 0
    
    print(rs)
    # Estimate run time is 180+ hours    
    """
    
    
def most_active(db):
    print("4. Who are the most active Twitter users (top ten)?")
    pipeline = [
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("user", -1)])},
        {"$limit": 10}
    ]
    result = db.tweets.aggregate(pipeline)
    pp_all(result)


def most_polarity(db):
    print("5. Who are the five most grumpy (most negative tweets) and the most happy (most positive tweets)?")
    print("5 most happy:")
    pipeline = [
        {"$match": {"polarity": "4"}},
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("user", -1)])},
        {"$limit": 5}
    ]
    result_happy = db.tweets.aggregate(pipeline)
    
    pp_all(result_happy)
    
    print("5 most grupmy:")
    pipeline = [
        {"$match": {"polarity": "0"}},
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("user", -1)])},
        {"$limit": 5}
    ]
    result_grumpy = db.tweets.aggregate(pipeline)
    
    pp_all(result_grumpy)


def pp_all(col):
    for p in col:
        pprint(p)

    
if __name__ == "__main__":
    main()