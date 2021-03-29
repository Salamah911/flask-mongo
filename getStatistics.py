import datetime
import psutil
import os
# from pymongo import MongoClient
import app
# def get_db():
#     client = MongoClient(host='mongodb',
#                          port=27017, 
#                          username='root', 
#                          password='pass',
#                          authSource="admin")
#     db = client.stats_db
#     return db

# db = app.get_db()

os.environ['MONGODB_PORT'] = str(app.env()[0])
os.environ['MONGODB_USERNAME'] = app.env()[1]
os.environ['MONGODB_PASSWORD'] = app.env()[2]
time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')
cpu_usge = psutil.cpu_percent()
memory_usge = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent
myDict = { "Time": time , "CPU_Usage" : cpu_usge , "Memory_Usage": memory_usge, "Disk_Usage" : disk_usage }
# db.stats_db.insert(myDict)
# db.connection.close
# app.insert_into_db(myDict)
file = open("/root/ss.txt", "w+")
a = file.write(str(myDict))
file.close()
app.insert_into_db(myDict)
print("inserted")
