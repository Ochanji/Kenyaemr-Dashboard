# %%
# Packages
from multiprocessing.spawn import prepare
from sqlalchemy import create_engine, text
import mysql.connector
import pandas as pd
# ------------------------------------------------------------------------------------
# %%
# Creat provider table in kenyaemr_etl table
url = 'mysql+pymysql://vin:Vin123**@127.0.0.1:3306'
engine = create_engine(url, echo=True)

querry1 = open(r'sql_queries/etl_provider table.sql').read().split(';\n')
for line in querry1:
    line 

sql1 = text('USE kenyaemr_etl')
engine.execute(sql1)

sql2 = text('DROP TABLE IF EXISTS etl_provider')
engine.execute(sql2)

sql3 = text('CREATE TABLE etl_provider (creator_id VARCHAR(50), provider VARCHAR(50))')
engine.execute(sql3)

sql4 = text(line)
engine.execute(sql4)

querry2 = open(r'sql_queries/PREP.sql').read().split(';\n')
for line2 in querry2:
    line2

querry3 = open(r'sql_queries/PREP ct.sql').read().split(';\n')
for line3 in querry3:
    line3

sql5 = text(line2)
results1 = engine.execute(sql5)

sql6 = text(line3)
results2 = engine.execute(sql6)

prep = pd.DataFrame(results1.fetchall())

prepct = pd.DataFrame(results2.fetchall())

df_prep = pd.merge(left=prep, right=prepct, how='left', on='patient_id')

# %%
# Connection Instance
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="vin",
    password="Vin123**",
    database="kenyaemr_etl")

mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")
for tables in mycursor:
    print(tables)

# %%
bins = [0, 14, 19, 24, 29, 34, 39, 44, 49, 1000]
labels = ['14yrs & below', '18-19yrs', '20-24yrs', '25-29yrs',
          '30-34yrs', '35-39yrs', '40-44yrs', '45-49yrs', '50+yrs']
          

# %%
# Overview Data
sql_query1 = open(
    r'sql_queries/overview.sql').read().split(';\n')

for a in sql_query1:
    print(a)

extract1 = pd.read_sql(a, mydb)
df_overview = pd.DataFrame(extract1)

df_overview['AgeGroup'] = pd.cut(
    df_overview['Age'], bins=bins, labels=labels, right=False)

# %%
# C&T Data
sql_query2 = open(
    r'sql_queries/ct.sql').read().split(';\n')

for b in sql_query2:
    print(b)

extract2 = pd.read_sql(b, mydb)
df_ct = pd.DataFrame(extract2)
df_ct = df_ct.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')
df_ct['AgeGroup'] = pd.cut(
    df_ct['Age'], bins=bins, labels=labels, right=False)

# %%
# HTS Data
sql_query3 = open(
    r'sql_queries/HTS.sql').read().split(';\n')

for c in sql_query3:
    print(c)

extract3 = pd.read_sql(c, mydb)
df_hts = pd.DataFrame(extract3)

group1 = df_hts.groupby('Financial_Year')
# Steps_FY1 = group1.get_group('Steps_FY1')
# Steps_FY1 = Steps_FY1.drop_duplicates(
#     ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')
Steps_FY2 = group1.get_group('Steps_FY2')
Steps_FY2 = Steps_FY2.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')
# Steps_FY3 = group1.get_group('Steps_FY3')
# Steps_FY3 = Steps_FY3.drop_duplicates(
#     ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

Steps_FY4 = group1.get_group('Steps_FY4')
Steps_FY4 = Steps_FY4.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

Steps_FY5 = group1.get_group('Steps_FY5')
Steps_FY5 = Steps_FY5.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

Vukisha_FY1 = group1.get_group('Vukisha_FY1')
Vukisha_FY1 = Vukisha_FY1.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

frames = [Steps_FY2, Steps_FY4, Steps_FY5, Vukisha_FY1]
df_hts = pd.concat(frames)

df_hts['AgeGroup'] = pd.cut(
    df_hts['Age'], bins=bins, labels=labels, right=False)

# %%
# Prevention
sql_query4 = open(
    r'sql_queries/prevention.sql').read().split(';\n')

for d in sql_query4:
    print(d)

extract4 = pd.read_sql(d, mydb)
df_prevention = pd.DataFrame(extract4)


group2 = df_prevention.groupby('Financial_Year')
# Steps_FY1 = group1.get_group('Steps_FY1')
# Steps_FY1 = Steps_FY1p.drop_duplicates(
#     ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')
Steps_FY2p = group2.get_group('Steps_FY2')
Steps_FY2p = Steps_FY2p.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')
# Steps_FY3 = group1.get_group('Steps_FY3')
# Steps_FY3 = Steps_FY3p.drop_duplicates(
#     ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

Steps_FY4p = group2.get_group('Steps_FY4')
Steps_FY4p = Steps_FY4p.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

Steps_FY5p = group2.get_group('Steps_FY5')
Steps_FY5p = Steps_FY5p.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

Vukisha_FY1p = group2.get_group('Vukisha_FY1')
Vukisha_FY1p = Vukisha_FY1p.drop_duplicates(
    ['First Name', 'Middle Name', 'Last Name', 'Age', 'Gender'], keep='first')

frames2 = [Steps_FY2p, Steps_FY4p, Steps_FY5p, Vukisha_FY1p]
df_prevention = pd.concat(frames2)

df_prevention['AgeGroup'] = pd.cut(
    df_prevention['Age'], bins=bins, labels=labels, right=False)
# %%
