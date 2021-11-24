import pymysql
import subprocess
import datetime
import re
from threading import Thread
import time


def ping():
    class SQL:
        def __init__(self):
            self.connection = pymysql.connect(
                host='192.168.88.49',
                user='root',
                password='12wqasxz',
                port=10002,
                cursorclass=pymysql.cursors.DictCursor)


    def ping_modem(name, hostname, command):
        dt_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            output = str(subprocess.check_output(command + hostname, shell=True))
            status = 'online'
            loss = re.findall(r'\S{0,8}%', output)[0]
            cursor.execute(f"INSERT INTO `webapp`.`log_modem` SET `datetime`='{dt_now}', `station`='{name}', `status`='{status}', `packet_loss`='{loss}'")
        except:
            loss = '100%'
            status = 'offline'
            cursor.execute(f"INSERT INTO `webapp`.`log_modem` SET `datetime`='{dt_now}', `station`='{name}', `status`='{status}', `packet_loss`='{loss}'")


    with SQL().connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM webapp.stations WHERE script = 1")
        data_ip = cursor.fetchall()

        if __name__ == '__main__':
            procs = []
            for item in data_ip:
                name = item['station_name']
                command = "ping -c 10 "
                hostname = item['ip_modem']
                proc = Thread(target=ping_modem, args=(name, hostname, command, ))
                procs.append(proc)
                proc.start()
                time.sleep(3)
            for proc in procs:
                proc.join()
        cursor.execute('commit')
        cursor.close()   
ping()
