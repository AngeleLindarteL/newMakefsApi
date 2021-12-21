from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://makefs:Kodastr2021!@makefs-user-data.zjijo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
ca = certifi.where()

conn = MongoClient(MONGO_URI, tlsCAFILE=ca)

userdb = conn.makefsUserData

userDC = userdb.usersData