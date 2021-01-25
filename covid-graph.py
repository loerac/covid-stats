#!/usr/bin/python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
from datetime import datetime as dt

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', help='Region from United States of America')
parser.add_argument('-s', '--save', help='Save the graph image', action='store_true')
parser.add_argument('-g', '--graph', help='Display the graph image', action='store_true')
parser.add_argument('-stat', '--statistics', help='Display weekly statistics', action='store_true')
args = parser.parse_args()

# Check if user passed a region
# If not, let the user know and exit
if args.region is None:
    print('Error: Region needed\n')
    parser.print_help()
    exit()

# Capitalize the first character in each word
region = ""
for r in args.region.split(' '):
    region += r.capitalize() + ' '
region = region[:-1]

df = pd.DataFrame(columns=['State', 'Date', 'Positive', 'Negative', 'Death'])

# Connect to database and get all the data for the the region
conn = psycopg2.connect(database='covid',
                        user='postgres',
                        password='password',
                        host='127.0.0.1',
                        port= '5432'
)
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM regions WHERE state='{region}'")

results = cursor.fetchall();
if len(results) == 0:
    print(f'{region} was not found in United States of American')
    exit()

for result in results:
    date = str(result[1][:4]) + '-' + str(result[1][4:6]) + '-' + str(result[1][6:])
    data = {
        'State': result[0],
        'Date': date,
        'Positive': result[2],
        'Negative': result[3],
        'Death': result[4],
    }

    if args.statistics:
        data['Hospitalized'] = result[5]
        data['ICU'] = result[6]
        data['Ventilator'] = result[7]
        data['Recovered'] = result[8]
        data['Positive Increase'] = result[9]
        data['Death Increase'] = result[10]

    df = df.append(data, ignore_index=True)

df['Positive Increase Percent'] = df['Positive'].pct_change() * 100
df['Positive Increase Percent'] = df['Positive Increase Percent'].round(decimals=3)
df['Positive Increase Percent'] = df['Positive Increase Percent'].astype(str) + ' %'

df['Death Increase Percent'] = df['Death'].pct_change() * 100
df['Death Increase Percent'] = df['Death Increase Percent'].round(decimals=3)
df['Death Increase Percent'] = df['Death Increase Percent'].astype(str) + ' %'
print(df.iloc[-1])

if args.save or args.graph:
    dates = df['Date']
    dates = [dt.strptime(str(d),'%Y-%m-%d').date() for d in dates]

    fig, ax_1 = plt.subplots()

    ax_1.plot(dates, df['Positive'], color='red', label='Positive Cases')
    ax_1.plot(dates, df['Negative'], color='green', label='Negative Cases')
    ax_1.set_ylabel('Test done in 100,000')
    ax_1.set_xlabel('Timeline')
    ax_1.tick_params(labelrotation=30)

    ax_2 = ax_1.twinx()
    ax_2.bar(dates, df['Death'], color='black', label='Death', alpha=0.5)
    ax_2.set_ylabel('Deaths')

    fig.set_figheight(12)
    fig.set_figwidth(13)
    fig.suptitle(f'{region} COVID-19 Cases')
    fig.legend(loc='upper left', fontsize=10)

    if args.save:
        plt.savefig(f'{region}.png')
    elif args.graph:
        plt.show()

conn.close()
