# Assignment 2 - Analysis of Twitter Data

This program should be able to do the following:

1. Import data from a csv file into a mongo database
2. Tell how many Twitter users are in the database?
2. Tell which Twitter users link the most to other Twitter users? (Provide the top ten.)
3. Tell who is are the most mentioned Twitter users? (Provide the top five.)
4. Tell who are the most active Twitter users (top ten)?
5. Tell who are the five most grumpy (most negative tweets) and the most happy (most positive tweets)?

This program uses the Twitter dataset from Sentiment140

[Link to the source](http://help.sentiment140.com/for-students/)

## Requirements

This program uses Python3, to run it correctly you must have Python3. 

It uses one non standart library, `pymongo`. In a bash terminal you can type `pip3 list | grep -F pymongo` to check if you have it installed. If you dont have it, you can type `pip3 install --user pymongo` to install it. 

## How to run the program

This program uses the standart library `argparse`, so if you type `python3 run.py -h` you'll get help text for the program. Here you can see positional arguments and optional arguments. Options in squared brackets are optional. 

To run the program, you'll first need to initalize it. This is done by typing `python3 run.py -i <csv file path>`.

When the database have been initialized, type `python3 run.py -r q [1-5]` to run one of the questions. E.g. `python3 run.py -r q 1` runs the first question

