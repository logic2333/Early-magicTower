#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 数据库交互

import psycopg2

conn = psycopg2.connect(dbname="MagicTower", user="postgres", password="SLCJUA", host="localhost", port="5432")
cur = conn.cursor()

def get_armor(_id):
    global cur
    cur.execute("SELECT * FROM \"装备\" WHERE \"标识符\" = %s", (_id, ))
    return cur.fetchone()

def get_special(_id):
    global cur
    cur.execute("SELECT * FROM \"特效\" WHERE \"编号\" = %s", (_id, ))
    return cur.fetchone()

def get_monster(_id):
    global cur
    cur.execute("SELECT * FROM \"怪物\" WHERE \"标号\" = %s", (_id, ))
    return cur.fetchone()

def get_user(_id):
    global cur
    cur.execute("SELECT * FROM \"用户\" WHERE \"用户名\" = %s", (_id, ))
    return cur.fetchone()

def register(_id, _pswd):
    global cur
    cur.execute("INSERT INTO \"用户\" VALUES (%s, %s, %s, %s, %s)", (_id, _pswd, None, None, 3))

def commit():
    global conn
    conn.commit()

def update_life(_id, _life_left):
    global cur
    cur.execute("UPDATE \"用户\" SET \"剩余复活次数\" = %s WHERE \"用户名\" = %s", (_life_left, _id))

def get_life(_id):
    global cur
    cur.execute("SELECT \"剩余复活次数\" FROM \"用户\" WHERE \"用户名\" = %s", (_id, ))
    return cur.fetchone()[0]

def reset_life(_id):
    global cur
    cur.execute("UPDATE \"用户\" SET \"剩余复活次数\" = 3 WHERE \"用户名\" = %s", (_id, ))
