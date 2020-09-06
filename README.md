pyExaMon is custom python script loads monitoring data from Exasol Database to InfluxDB for Grafana.


###### Please note that this is an open source project which is *not officially supported* by EXASOL.

Create InfluxDb manually before using this script.


```
Connected to http://localhost:8086 version 1.8.2
InfluxDB shell version: 1.8.2
> create database pyexamon
> show databases
name: databases
name
----
_internal
pyexamon
>
```


## System requirements (tested with)
Exasol >= 6

Python >= 3.6

pyexasol >= 0.14.1

influxdb-python >= 5.3.0


## ToDo
Transaction conflicts count for a last day

User sessions count

Idle sessions count

Add short in-picture manual how to add panel to the dashboard


## Created by
Vladimir Gerasimov, 2020
