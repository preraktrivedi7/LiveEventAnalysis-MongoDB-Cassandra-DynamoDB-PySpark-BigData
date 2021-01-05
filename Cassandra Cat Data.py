import requests 
import json 
import MySQLdb 
CONSUMER_KEY = "" 
CONSUMER_SECRET = ""
 ACCESS_TOKEN = "" 
ACCESS_TOKEN_SECRET = ""
 
HOST = "localhost"
 USER = "newuser" 
PASSWD = "" 
DATABASE = "AirQuality" 
 
 
request = requests.get('https://cat-fact.herokuapp.com/facts')
abcd = json.loads(request.text) print((abcd['all'])) 
for element in abcd['all']:    
 id=element['_id'] 
 type = element['type']     
 upvotes = element['upvotes']     
#insert query    
db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")   
cursor = db.cursor()     
insert_query = "INSERT INTO cat (id, type, upvotes) VALUES (%s, %s, %s)"    
cursor.execute(insert_query, (id, type, upvotes))     
db.commit()    
print("Cat data stored in SQL")     
db.commit() 
 
cursor.close()

db.close() 
#type(eval(abcd)) 
 
print(request.status_code)   