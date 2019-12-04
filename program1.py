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
print(InventoryID_SumParts)





# prompt user to see which parts they need 
getMoreInfo = input("Do you want to see what parts you need for non-full sets?   Enter yes or no: ")
if getMoreInfo == "yes":
    getMissing = input("Enter the set number to see which parts you need: ")



# find inventory ID from set_num
cur.execute("select inventory_id from inventories where set_num = " + "'" + getMissing + "'" + ";")
InvenID = cur.fetchall()
InvenID = clean(InvenID)

# Find all parts from the set of interest:
cur.execute("select part_num from inventory_parts where inventory_id = " + str(InvenID[0]) + ";")
MissingParts = cur.fetchall()

# loop through list and see which parts we don't have 
# run time is O(n), can probably reduce to O(logN)
Needed = []
for i in ALLPartsList:
    if i not in MissingParts:
        Needed.append(i)
    else:
        pass

print(Needed)


