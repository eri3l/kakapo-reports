#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:27:31 2023

@author: eriel
"""
import streamlit as st
#import numpy as np
import pandas as pd

st.title("Search for bird by tx channel or id")

#### prep ####

### get data ###
records_tx = pd.read_csv("dat/processed/31-03-2023-records_tx.csv")
st.subheader('Manipulated transmitter records')
st.dataframe(records_tx.head())

#### search ####
st.subheader('Case 1. Given a txDuskyId, return list of all records for it')

myTxDuskyId = st.text_input("Search by transmitter id: ")
st.write('Searching by transmitter id: ', myTxDuskyId)

resCase1 = records_tx[records_tx['txFromDuskyId'] == myTxDuskyId]
resCase1 = resCase1[['birdName', 'txFromDuskyId', 'txChannel','txDateOn', 'txDateOff', 'island']]

st.table(resCase1)

##
st.subheader('Case 2 . given a txChannel, return list (birdName, date, txid)')
myTxCh = st.number_input("Search by transmitter channel: ")

resCase2 = records_tx[records_tx['txChannel'] == myTxCh]
resCase2 = resCase2[['birdName', 'txFromDuskyId', 'txChannel','txDateOn', 'txDateOff', 'island']]

st.write(resCase2)

## 
st.subheader('Case 3. (island) Given a txChannel or txDuskyId and/or island, return bird list')

myTxChCase3 = st.number_input("Enter transmitter channel: ")
myIsland = st.text_input("Enter island: ")

# myIsland = "Whenua Hou"
resCase3 = records_tx[(records_tx['txChannel'] == myTxChCase3 ) & (records_tx['island'] == myIsland)]

resCase3 = resCase3[['birdName', 'txFromDuskyId', 'txChannel','txDateOn', 'txDateOff', 'island']]

st.dataframe(resCase3)