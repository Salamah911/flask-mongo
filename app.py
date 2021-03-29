from flask import Flask, jsonify, render_template
import psutil
from crontab import CronTab
from pymongo import MongoClient
import pymongo
import datetime
import json
import os
import logging
import requests


app = Flask(__name__)


from functools import wraps
def log_function_data(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))
        str = f"At {now} -> calling: {fn.__name__}, doc: {fn.__doc__} \n"
        print (str)  
        file = open("traces.log", "a")
        file.write(str)
        return fn(*args, **kwargs)
    return wrapper

@log_function_data
def get_db():
    """ Detects the running database """
    client = MongoClient(host='mongodb',
                         port=int(os.environ['MONGODB_PORT']), 
                         username=os.environ['MONGODB_USERNAME'], 
                         password=os.environ['MONGODB_PASSWORD'],
                         authSource="admin")
    db = client.stats_db
    return db

def env():
    return [int(os.environ['MONGODB_PORT']), os.environ['MONGODB_USERNAME'] , os.environ['MONGODB_PASSWORD']]


@log_function_data
def insert_into_db(data):
    """ Inserts object to database """
    db = get_db()
    db.stats_db.insert(data)
    return 

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s <br>')
@app.route("/status", methods=['GET'])
@log_function_data
def health_check():
    """ Function to print all recorded logs from record.log """
    file = open("record.log")
    return file.read()

@app.route('/')
@log_function_data
def home_page():
    """ home page, no API """
    return render_template('index.html')

@app.route('/current_cpu', methods=['GET'])
@log_function_data
def get_current_cpu():
    """ get current read of cpu statistics , API = GET"""
    cpu_usge = psutil.cpu_percent()
    str = f"cpu usage for the current time is : {cpu_usge}% "
    return render_template('current_cpu.html', variable=str)


@app.route('/current_memory', methods=['GET'])
@log_function_data
def get_current_memory():
    """ get current read of memory statistics , API = GET"""
    memory_usge = psutil.virtual_memory().percent
    str = f"memory usage for the current time is : {memory_usge}% "
    return render_template('current_memory.html', variable=str)


@app.route('/current_disk', methods=['GET'])
@log_function_data
def get_current_disk():
    """ get current read of disk statistics , API = GET"""
    disk_usage = psutil.disk_usage('/').percent
    str = f"disk usage for the current time is : {disk_usage}% "
    return render_template('current_disk.html', variable=str)

@app.route('/cpu_stats', methods=['GET'])
@log_function_data
def get_cpu_stats():
    """ get last 24 hours cpu statistics , API = GET"""
    db = get_db()
    _stats = db.stats_db.find({}, { "_id": 0, "Memory_Usage": 0, "Disk_Usage": 0 } )
    stats = [str(item) for item in _stats]
    Dict = {}
    stat = set()
    for item in stats:
        Dict = eval(item)
        date = datetime.datetime.strptime(str(Dict['Time']), '%Y-%m-%d-%H:%M')
        date1 = datetime.datetime.now()
        yesterday = date1 - datetime.timedelta(days=1)
        if(date > yesterday):
            stat.add(item)
    stats = [str(item).replace('"', '').replace("'","").replace("{","").replace("}","") for item in stat]
    stats.sort()
    return render_template('cpu_stats.html', items=stats)


@app.route('/disk_stats', methods=['GET'])
@log_function_data
def get_disk_stats():
    """ get last 24 hours memoyr statistics , API = GET"""
    db = get_db()
    _stats = db.stats_db.find({}, { "_id": 0, "CPU_Usage": 0, "Memory_Usage": 0 } )
    stats = [str(item) for item in _stats]
    Dict = {}
    stat = set()
    for item in stats:
        Dict = eval(item)
        date = datetime.datetime.strptime(str(Dict['Time']), '%Y-%m-%d-%H:%M')
        date1 = datetime.datetime.now()
        yesterday = date1 - datetime.timedelta(days=1)
        if(date > yesterday):
            stat.add(item)
    
    stats = [str(item).replace('"', '').replace("'","").replace("{","").replace("}","") for item in stat]
    stats.sort()
    return render_template('disk_stats.html', items=stats)

@app.route('/memory_stats', methods=['GET'])
@log_function_data
def get_memory_stats():
    """ get last 24 hours disk statistics , API = GET """
    db = get_db()
    _stats = db.stats_db.find({}, { "_id": 0, "Disk_Usage": 0, "CPU_Usage": 0 } )
    
    #stats = [str(item).replace('"', '').replace("'","").replace("{","").replace("}","") for item in _stats]
    stats = [str(item) for item in _stats]
    Dict = {}
    stat = set()
    for item in stats:
        Dict = eval(item)
        date = datetime.datetime.strptime(str(Dict['Time']), '%Y-%m-%d-%H:%M')
        date1 = datetime.datetime.now()
        yesterday = date1 - datetime.timedelta(days=1)
        if(date > yesterday):
            stat.add(item)
    stats = [str(item).replace('"', '').replace("'","").replace("{","").replace("}","") for item in stat]
    stats.sort()
    return render_template('memory_stats.html', items=stats)


if __name__=='__main__':
    app.run("0.0.0.0",5000, debug=True)
