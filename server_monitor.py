#!/usr/bin/python2.5
"""
Monitoring memory and cpu
"""
import os
import sqlite3 as db
import time

CONEXION = db.connect("servers.db")
CRSR = CONEXION.cursor()

DAT_TIME = time.strftime('%Y-%m-%d %H:%M:%S')
DAT_HNAM = os.popen('uname -n').read().strip()
DAT_KERN = os.popen('uname -r').read().strip()

#Memory
DAT = os.popen("""egrep '(MemTotal|MemFree|SwapTotal|SwapFree):' 
    /proc/meminfo """)
DAT_MEM = [data.split(':')[1].strip().split(' ')[0] for data in DAT]
SQL = """insert into memoria (hostname,date_time,kernel,mem_total,
    mem_free,swap_total,swap_free) values ('%s','%s','%s','%s','%s',
    '%s','%s')""" % (DAT_HNAM, DAT_TIME, DAT_KERN, DAT_MEM[0],
    DAT_MEM[1], DAT_MEM[2], DAT_MEM[3])
CRSR.execute(SQL)

#CPU
DAT = os.popen("mpstat -P ALL").readlines()
DAT_TMP = [data.strip().split(' ') for data in DAT[3:]]
for val in DAT_TMP:
    nli = []
    for ele in val:
        if ele and ':' not in ele:
            nli.append(ele)
    nli.insert(0, DAT_KERN)
    nli.insert(0, DAT_TIME)
    nli.insert(0, DAT_HNAM)
    sql = """insert into procesador (hostname,date_time,kernel,cpu_num,
        usr,nice,sys,iowait,irq,soft,steal,guest,idle) values ('%s',
        '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
        '%s')""" % tuple(nli)
    CRSR.execute(SQL)

CONEXION.commit()
CONEXION.close()

