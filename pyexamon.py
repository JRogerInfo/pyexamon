import pyexasol
import time
from influxdb import InfluxDBClient

# Settings section
###############################################################################

# InfluxDB connection
influx_db = {
    'host': '127.0.0.1',
    'port': '8086',
    'user': 'root',
    'pass': 'root',
    'db'  : 'exatest'
}

# Exasol DB(s) connection
exasol_dbs = {
    0:{'alias' : 'ExaDb_1', 'dsn' : '127.0.0.1:8563', 'user' : 'SYS', 'pass' : 'exasol'},

    # You can add more than one DB
    1:{'alias' : 'ExaDb_2', 'dsn' : '192.168.56.2:8563', 'user' : 'SYS', 'pass' : 'exasol'},

    # 2:{'host' : '192.168.1.11', 'port' : '8563', 'user' : 'SYS', 'pass' : 'exasol'},
    # ...
    # xxx:{'host' : '192.168.1.xxx', 'port' : '8563', 'user' : 'SYS', 'pass' : 'exasol'}
}

# Loop after xxx seconds
time_to_sleep = 30


# Subroutines section
###############################################################################

def exa_connect(dsn, user, password):

    try:
        exa_conn = pyexasol.connect(dsn=dsn, user=user, password=password)

#TODO add right exceptions for Exasol
    except:
        print ("Can't connect to Exasol DB at", dsn, "Skiping...")
        return None
    
    return exa_conn


def influx_connect(host, port, user, password, database):

    try:
        influx_conn = InfluxDBClient(host, port, user, password, database)

#TODO add right exceptions for Influx
    except:
        print ("Can't connect to InfluxDB at", host)
        print ("Exiting.")
        exit(1)

    return influx_conn


def get_exa_monitor_last_day(conn, limit):

    str_limit = str(round(limit))
    sql_query = "SELECT * FROM EXA_MONITOR_LAST_DAY ORDER BY MEASURE_TIME DESC LIMIT " + str_limit

    try:
        records = conn.execute(sql_query)

#TODO add right exceptions for Exasol
    except:
        print ("Can't query ExaDB. Skipping...")
        return None

    return records


def load_records_into_influxdb(records, influx_conn, exa_alias):

    try:
        for row in records.fetchall():

            json_body = [
                {
                    "measurement": "EXA_MONITOR_LAST_DAY",
                    "tags": {
                        "host": exa_alias,
                    },
                    "time": row[0],
                    "fields": {
                        "host": exa_alias,
                        "load": row[1],
                        "cpu": row[2],
                        "temp_db_ram": row[3],
                        "hdd_read": row[4],
                        "hdd_write": row[5],
                        "net": row[6],
                        "swap": row[7]
                    }
                }
            ]

        influx_conn.write_points(json_body)

#TODO add right exceptions for Influx and Exasol
    except:
        print ("Something is going wrong")



# Main code section
###############################################################################

# In case of loop_mode do this code inifinitelly
while True:

    # How many records we should get.
    records_to_get = time_to_sleep/60+2

    # InfluxDB connection
    iconn = influx_connect(influx_db["host"], influx_db["port"], influx_db["user"], influx_db["pass"], influx_db["db"])

    # For every Exasol DB
    for db_index in exasol_dbs:

        # Ecasol connection
        econn = exa_connect(exasol_dbs[db_index]["dsn"], exasol_dbs[db_index]["user"], exasol_dbs[db_index]["pass"])

        # If connection exists
        if (econn != None):

            # Loading records to InfluxDb
            records = get_exa_monitor_last_day(econn, records_to_get)

            load_records_into_influxdb(records, iconn, exasol_dbs[db_index]["alias"])

			# Closing Exa connection
            econn.close()

    # Wait a time then repeat
    time.sleep(time_to_sleep)


# Closing InfluxDB connection
iconn.close()
