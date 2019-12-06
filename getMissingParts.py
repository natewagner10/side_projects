#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:18:00 2019

@author: natewagner
"""
import psycopg2
conn = psycopg2.connect("dbname=LEGOS user=nwagner")
cur = conn.cursor()

from program1 import findOtherSets, clean

def getMissingParts(X, getMissing):
    '''
    Function takes in a lego set-number and outputs the parts you need to 
    build that set 
    
    '''
    
    
    ALLPartsList, setnums = findOtherSets(X, numToSee = 10, numFull = True)    
    # prompt user to see which parts they need 
    #getMoreInfo = input("Do you want to see what parts you need for non-full sets?   Enter yes or no: ")
    #if getMoreInfo == "yes":
    #getMissing = input("Enter the set number to see which parts you need: ")
    
    
    
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
    for i in MissingParts:
        if i[0] not in ALLPartsList:
            Needed.append(i)
        else:
            pass
    
    for x in Needed:
        print (x[0])
        

    

findOtherSets(numToSee = 10, numFull = True)
