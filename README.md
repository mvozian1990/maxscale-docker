# Database schema-based sharding with mariadb and maxscale

I'm setting up two mariaddb databases as sharding for maxscale in frong of them. Maxscale is managing both of them. The python script connects to maxscale and queries data from both databases, zipcode_one and zipcode_two.

## My project setup

In the Docker-compose file there are declared three services: two mariadb services and one maxscale service.
```
mariadb master1: port 4001
mariadb master2: port 4003
mariadb maxscale: port 4000
```

Maxscale know how to route the database requests based on the schema, because it is configured with the two database servers as shards with **schema routing**

## Pre-requisites needed
```
 -- docker
 -- docker-compose
 -- mariadb client
 -- python3
 ```
 
 ## Preparing
 ```
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt install docker-ce
sudo apt install docker-compose
sudo apt install mariadb-client
 ```
 
## Running services

To run the project, run form the maxscale folder:
**docker-compose up -d**

Here is what you'll see:
```
Creating network "maxscale_default" with the default driver
Creating maxscale_master2_1 ... done
Creating maxscale_master1_1 ... done
Creating maxscale_maxscale_1 ... done
```
// After some time it will start up, then run:
**docker-compose maxscale exec maxctrl list servers**
// Note the two mariadb servers running

```
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬───────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID      │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
│ server1 │ master1 │ 3306 │ 0           │ Master, Running │ 0-3000-4  │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
│ server2 │ master2 │ 3306 │ 0           │ Running         │ 0-3001-31 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴───────────┘
```
Go into maxscale on port 4000 and see both schemas present

**mariadb -h 127.0.0.1 -u maxuser -pmaxpwd -P 4000**

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| zipcodes_one       |
| zipcodes_two       |
+--------------------+

Now go into master1 on port 4001 and notice only zipcodes_one database is present

**mariadb -h 127.0.0.1 -u maxuser -pmaxpwd -P 4001**

```
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| zipcodes_one       |
+--------------------+
```

Similarly, the second master has the second schema:

**mariadb -h 127.0.0.1 -u maxuser -pmaxpwd -P 4003**

```
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| zipcodes_two       |
+--------------------+
```


## Running

To run the python script, go into the root directory, and run:

**python shard-query.py**

Here is the output:


Last 10 rows from zipcodes_one
```
(40843, 'STANDARD', 'HOLMES MILL', 'KY', 'PRIMARY', '36.86', '-83', 'NA-US-KY-HOLMES MILL', 'FALSE', '', '', '')
(41425, 'STANDARD', 'EZEL', 'KY', 'PRIMARY', '37.89', '-83.44', 'NA-US-KY-EZEL', 'FALSE', '390', '801', '10204009')
(40118, 'STANDARD', 'FAIRDALE', 'KY', 'PRIMARY', '38.11', '-85.75', 'NA-US-KY-FAIRDALE', 'FALSE', '4398', '7635', '122449930')
(40020, 'PO BOX', 'FAIRFIELD', 'KY', 'PRIMARY', '37.93', '-85.38', 'NA-US-KY-FAIRFIELD', 'FALSE', '', '', '')
(42221, 'PO BOX', 'FAIRVIEW', 'KY', 'PRIMARY', '36.84', '-87.31', 'NA-US-KY-FAIRVIEW', 'FALSE', '', '', '')
(41426, 'PO BOX', 'FALCON', 'KY', 'PRIMARY', '37.78', '-83', 'NA-US-KY-FALCON', 'FALSE', '', '', '')
(40932, 'PO BOX', 'FALL ROCK', 'KY', 'PRIMARY', '37.22', '-83.78', 'NA-US-KY-FALL ROCK', 'FALSE', '', '', '')
(40119, 'STANDARD', 'FALLS OF ROUGH', 'KY', 'PRIMARY', '37.6', '-86.55', 'NA-US-KY-FALLS OF ROUGH', 'FALSE', '760', '1468', '20771670')
(42039, 'STANDARD', 'FANCY FARM', 'KY', 'PRIMARY', '36.75', '-88.79', 'NA-US-KY-FANCY FARM', 'FALSE', '696', '1317', '20643485')
(40319, 'PO BOX', 'FARMERS', 'KY', 'PRIMARY', '38.14', '-83.54', 'NA-US-KY-FARMERS', 'FALSE', '', '', '')
```

First 10 rows from zipcodes_two
```
(42040, 'STANDARD', 'FARMINGTON', 'KY', 'PRIMARY', '36.67', '-88.53', 'NA-US-KY-FARMINGTON', 'FALSE', '465', '896', '11562973')
(41524, 'STANDARD', 'FEDSCREEK', 'KY', 'PRIMARY', '37.4', '-82.24', 'NA-US-KY-FEDSCREEK', 'FALSE', '', '', '')
(42533, 'STANDARD', 'FERGUSON', 'KY', 'PRIMARY', '37.06', '-84.59', 'NA-US-KY-FERGUSON', 'FALSE', '429', '761', '9555412')
(40022, 'STANDARD', 'FINCHVILLE', 'KY', 'PRIMARY', '38.15', '-85.31', 'NA-US-KY-FINCHVILLE', 'FALSE', '437', '839', '19909942')
(40023, 'STANDARD', 'FISHERVILLE', 'KY', 'PRIMARY', '38.16', '-85.42', 'NA-US-KY-FISHERVILLE', 'FALSE', '1884', '3733', '113020684')
(41743, 'PO BOX', 'FISTY', 'KY', 'PRIMARY', '37.33', '-83.1', 'NA-US-KY-FISTY', 'FALSE', '', '', '')
(41219, 'STANDARD', 'FLATGAP', 'KY', 'PRIMARY', '37.93', '-82.88', 'NA-US-KY-FLATGAP', 'FALSE', '708', '1397', '20395667')
(40935, 'STANDARD', 'FLAT LICK', 'KY', 'PRIMARY', '36.82', '-83.76', 'NA-US-KY-FLAT LICK', 'FALSE', '752', '1477', '14267237')
(40997, 'STANDARD', 'WALKER', 'KY', 'PRIMARY', '36.88', '-83.71', 'NA-US-KY-WALKER', 'FALSE', '', '', '')
(41139, 'STANDARD', 'FLATWOODS', 'KY', 'PRIMARY', '38.51', '-82.72', 'NA-US-KY-FLATWOODS', 'FALSE', '3692', '6748', '121902277')
```

Largest zipcode in zipcodes_one
```
(47750,)
```

Smallest zipcode in zipcodes_two
```
(38257,)
```

-------------------

Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```
# Sources
https://mariadb.com/kb/en/mariadb-maxscale-14/maxscale-simple-sharding-with-two-servers/
https://mariadb.com/kb/en/mariadb-maxscale-14/maxscale-routers-schemarouter-router/
https://dzone.com/articles/schema-sharding-with-mariadb-maxscale-21-part-2
