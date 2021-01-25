#!/usr/bin/python3

import psycopg2
import requests
import schedule
import time
from regions import Regions

def ValidData(data):
    if isinstance(data, int):
        return data
    return 0

def CreateTable():
    conn = psycopg2.connect(database='covid',
                            user='postgres',
                            password='password',
                            host='127.0.0.1',
                            port= '5432'
    )
    cursor = conn.cursor()
    sql = 'DROP TABLE IF EXISTS regions'
    print(f'CreateTable({sql})')
    cursor.execute(sql)

    sql = '''CREATE TABLE regions(
        state TEXT NOT NULL,
        date TEXT,
        positive INT,
        negative INT,
        deaths INT,
        hospitalized INT,
        icu INT,
        ventilator INT,
        recovered INT,
        positive_increase INT,
        death_increase INT
        )'''
    print(f'CreateTable({sql})')
    cursor.execute(sql)
    conn.commit()
    conn.close()

def AddResults(results):
    conn = psycopg2.connect(database='covid',
                            user='postgres',
                            password='password',
                            host='127.0.0.1',
                            port= '5432'
    )
    cursor = conn.cursor()

    for result in results:
        positive = ValidData(result['positive'])
        negative = ValidData(result['negative'])
        death = ValidData(result['death'])
        hospitalized = ValidData(result['hospitalizedCurrently'])
        icu = ValidData(result['inIcuCurrently'])
        ventilator = ValidData(result['onVentilatorCurrently'])
        recovered = ValidData(result['recovered'])
        pos_increase = ValidData(result['positiveIncrease'])
        death_increase = ValidData(result['deathIncrease'])

        sql = "INSERT INTO regions(state,  date, positive, negative, deaths, \
            hospitalized, icu, ventilator, recovered, positive_increase, death_increase) \
            VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
            .format(Regions[result['state']],
                    result['date'],
                    positive,
                    negative,
                    death,
                    hospitalized,
                    icu,
                    ventilator,
                    recovered,
                    pos_increase,
                    death_increase,
                )
        print(f'AddResults({sql})')
        cursor.execute(sql)
        conn.commit()
    conn.close()

def Historical():
    CreateTable()
    results = requests.get('https://api.covidtracking.com/v1/states/daily.json')
    results = results.json()
    results.reverse()

    AddResults(results)

def UpdateRegions():
    results = requests.get('https://api.covidtracking.com/v1/states/current.json')
    AddResults(results.json())

if __name__=="__main__":
    schedule.every().day.at('08:30').do(UpdateRegions, 'Snapshot activated...')
    Historical()

    while(1):
        schedule.run_pending()
        time.sleep(86400)
