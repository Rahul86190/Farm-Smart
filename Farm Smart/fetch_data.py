from pymongo import MongoClient 
connection_string= "mongodb+srv://rahulsaini132005:20QWO9wOz43Tj3Ur@newproject1.xuqcm.mongodb.net/?retryWrites=true&w=majority&appName=NEWproject1"
client = MongoClient(connection_string)
database = client['Farmer2']
collection = database['FarmerData1']

documents = collection.find()  # select * from table;
for document in documents: 
    print(document) 
print("thank you!") 

# execute this file to fectch your data from database 