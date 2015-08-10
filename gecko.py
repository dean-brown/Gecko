"""
Fools gold
"""
from threading import Thread
import urllib
import json
import time
import MySQLdb

# unix_socket="/run/mysqld/mysqld.sock")

# Set the globals:
        
log_file = open('log.txt', 'a')


def th(ur):
    base = 'http://www.bloomberg.com/markets/chart/data/1D/' + ur + ':us'
    html_text = urllib.urlopen(base)
    data = json.load(html_text)
    data_points = data["data_values"]
    # Should print the current value:
    try:
        print "[+] The price of: " + str(ur) + " is " + str(data_points[len(data_points) - 1][1])

        # Insert into the database:
        
        con = MySQLdb.connect(user='root', passwd='Welcome2', db='gecko_test',
                host='localhost') 
       	
        cur = con.cursor()
        cur.execute("INSERT INTO stock(name, value) VALUES (%s, %s)", 
                (str(ur), str(data_points[len(data_points) - 1][1])))
        
        con.commit()
        con.close()
        
        print "[+] Database has been updated"    
        print "[+] Dumping to log file"    
        log_file.write(str("Name " + str(ur) + "\nValue: " + str(data_points[len(data_points) - 1][1])))    
    
    
    except Exception, e:
        # Print the stocks that cause issues to another file!
        print "Problem with: " + str(ur)
        print "The exception seems to relate to: " + str(e)
        print "[+] Dumping error details to log file"
        log_file.write("Exception details: " + str(e))

start_time = time.time()
symbol_list = open("stocksymbols.txt").read()
symbol_list = symbol_list.split("\n")

thread_list = []

for symbol in symbol_list:
    t = Thread(target=th, args=(symbol,))
    t.start()
    thread_list.append(t)

for b in thread_list:
    b.join()

print "[+] Elapsed time: %s" % (start_time - time.time())
con.close()
print "[*] Connection closed"


#69th line for the lulz ><
