#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 12:27:11 2019

@author: natewagner
"""

#
import psycopg2
conn = psycopg2.connect("dbname=LEGOS user=nwagner")
cur = conn.cursor()


# User will input the set_nums from sets that they have
setnums = input("Please enter the set_num associated with the set you have, seperated by a comma: ")
setnums = "0013-1, 0013-10, 0055-1, 00222-1, 0009995-1"

setnums = str(setnums)
if len(setnums) > 1:
    setnums = setnums.split(",")
    setnums = [x.replace(' ', '') for x in setnums]


# clean the user input
setnums = setnums.split(",")
setnums = [x.replace(' ', '') for x in setnums]


# initiate query to obtain inventory_id's form the corresponding set_nums
InventoryID = "select inventory_id from inventories where set_num = " + "'" + setnums[0] + "'"

# create query:
# this adds the " or set_num =  " to end of the query depending on how many sets the user has
for i in range(1, len(setnums)):
    whereStatement = " or set_num = " + "'" + setnums[i] + "'" 
    if len(setnums) == 1:
        InventoryID = "select inventory_id from inventories where set_num = " + "'" + setnums + "'" 
    else:
        InventoryID = InventoryID + whereStatement
    
# finalize query:
InventoryID = InventoryID + ";"

# execute SQL command:
cur.execute(InventoryID)
InventoryIDS = cur.fetchall()





#InventoryIDS = [(1414,), (4609,), (5004,), (12208,)]
# select * from inventory_parts where inventory_id = 1414 or inventory_id = 4609 or inventory_id = 5004 or inventory_id = 12208;

# function to clean the results from a query:
def clean(i):
    holder = []
    for x in range(0, len(i) ):
        holder.append(i[x][0])
    return holder
    

IDs = clean(InventoryIDS)

# intialize query to get the associated parts and how many:
PartsList = "select part_num from inventory_parts where inventory_id = " + str(IDs[0])

# create query:
# this adds the additional inventory_ids to end of query:
for i in range(1, len(IDs)):
    whereStatement = " or inventory_id = " + str(IDs[i])
    if len(IDs) == 1:
        PartsList = "select part_num from inventory_parts where inventory_id = " + str(IDs) 
    else:
        PartsList = PartsList + whereStatement

# finalize query:
PartsList = PartsList + ";"

# execute in SQL
cur.execute(PartsList)
ALLPartsList = cur.fetchall()




# clean parts
ALLPartsList = clean(ALLPartsList)

#ALLPartsList = [('3626apr0001',), ('3838',), ('3842a',), ('3962a',), ('970c00',), ('973p90c02',), ('3626apr0001',)]
#ALLPartsList = clean(ALLPartsList)

# select inventory_id, sum(quantity) from (select inventory_id, part_num, quantity from inventory_parts where part_num = '3626apr0001' or part_num = '3838' or part_num = '3842a' or part_num = '3962a' or part_num = '970c00' or part_num = '973p90c02') hold group by hold.inventory_id order by sum desc;

# initialize query to get quantity of parts we have
GetParts = "select inventory_id, part_num, quantity from inventory_parts where part_num = " + "'" + ALLPartsList[0] + "'" 


# create query:
# this adds the additional part_nums to end of query:
for i in range(1, len(ALLPartsList)):
    whereStatement = " or part_num = " + "'" + str(ALLPartsList[i]) + "'" 
    if len(ALLPartsList) == 1:
        GetParts = "select inventory_id, part_num, quantity from inventory_parts where inventory_id = " + "'" + str(ALLPartsList) + "'" 
    else:
        GetParts = GetParts + whereStatement




cur.execute("select set_num, set_name, sum/num_parts::float*100 as percentParts from (select a.set_num, a.sum, b.set_name, b.num_parts from (select a.set_num, b.sum from inventories a, (select inventory_id, sum(quantity) from (" + GetParts + ") hold group by hold.inventory_id order by sum desc) b where a.inventory_id = b.inventory_id) a, sets b where a.set_num = b.set_num) a order by percentParts desc limit 10;")
InventoryID_SumParts = cur.fetchall()
print("select set_num, set_name, sum/num_parts::float*100 as percentParts from (select a.set_num, a.sum, b.set_name, b.num_parts from (select a.set_num, b.sum from inventories a, (select inventory_id, sum(quantity) from (" + GetParts + ") hold group by hold.inventory_id order by sum desc) b where a.inventory_id = b.inventory_id) a, sets b where a.set_num = b.set_num) a order by percentParts desc limit 10;")








