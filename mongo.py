from pymongo import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import pandas as pd

# Mongo DB Store
uri = "mongodb+srv://anaybhat:DNffDG6xV9vyr9SQ@cluster0.knvvmat.mongodb.net/"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['client']
collection = db['collection']
documents = collection.find()
documents_list = list(documents)

values = [[doc['ligand'].split('/')[1].split('.')[0], doc['receptor'].split('/')[1].split('.')[0], float(doc['affinity'])] for doc in documents_list]
values_array = np.array(values)
df = pd.DataFrame(values_array, columns=['Ligand', 'Receptor', 'Affinity'])
df.to_csv('df.csv', index=False)
# print(df)