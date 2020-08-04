import os 
import csv 
import time 
import locale 
from re import sub
from decimal import Decimal
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
import requests
import psycopg2

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.xml", "*.csv"]

    def __init__(self, conn):
        self.conn = conn
        super().__init__() 

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print("process")
        print(event.src_path, event.event_type) # print now only for degug
        filename_w_ext = os.path.basename(event.src_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        print(filename)
        cur = self.conn.cursor() 
        with open(event.src_path) as csv_file:
            n = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader: 
                if n == 0: 
                    n = n + 1 
                    continue 
                if row[0] not in ["233044500", "X70974968"]: 
                    continue 
                dictRow = {} 
                dictRow["account"]   = row[0]
                dictRow["symbol"]    = row[1]
                print(row[12]) 
                row[12] = row[12].replace("n/a", "0")
                row[6] = row[6].replace("n/a", "0")
                dictRow["costbasis"] = Decimal(sub(r'[^\d.]', '', row[12])) 
                dictRow["curvalue"]  = Decimal(sub(r'[^\d.]', '', row[6])) 
                print(dictRow) 
                s = "insert into agni_etl_stage_ff1(asofdate,accname,symbol,costbasis,currentvalue)values(%s,%s,%s,%s,%s);"
                data = (filename, dictRow["account"], dictRow["symbol"], dictRow["costbasis"], dictRow["curvalue"])
                cur.execute(s, data) 
                self.conn.commit() 

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        print("created") 
        #self.process(event)

city = "New-York"
print("I am from " + city)
r = requests.get('http://www.google.com')
print(r.status_code)
print(os.environ["TEST"]) 
conn = psycopg2.connect(
   database="agni_etl_dev", 
   user = "postgres", 
   password = "postgres", 
   host = "db", 
   port = "5432"
)

cur = conn.cursor()
cur.execute("SELECT col1 from test1")
rows = cur.fetchall()
print(rows)

observer = Observer()
observer.schedule(MyHandler(conn), path='./data')
observer.start()

#try: 
#    print("sleeping")
#    # time.sleep(5)
#    print("wake")
#except KeyboardInterrupt:
#    observer.stop()
#time.sleep(10)
#observer.stop()
observer.join()
conn.close()

