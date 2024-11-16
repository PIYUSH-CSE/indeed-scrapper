import pandas as pd
import pymongo
import json


def load():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    df = pd.read_csv('final.csv')
    data = df.to_dict(orient="records")

    db = client["indeed_jobs"]

    res = db.python_developer_jobs.insert_many(data)
    print("Result Inserted")