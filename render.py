#!/usr/bin/env python
#
# render.py - Renders maps

import os, sys, zipfile, re, json
import subprocess
from subprocess import call
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ALT_DB_NAME = os.environ.get("ALT_DB_NAME")
ALT_DB_USER = os.environ.get("ALT_DB_USER")
ALT_DB_PASS = os.environ.get("ALT_DB_PASS")
ALT_DB_HOST = os.environ.get("ALT_DB_HOST")
ALT_DB_PORT = os.environ.get("ALT_DB_PORT")
codebase = os.environ.get("CODEBASE_PATH")

print("Updating codebase repository...")
call("git pull".split(), shell=False, cwd=codebase)
repohash = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],stdout=subprocess.PIPE, cwd=codebase)
repohash = repohash.stdout.decode('UTF-8')

# I'd like to do a hard reset and pull, but IN THEORY no changes should ever be
# made to the local repository
# 

maps = []

connstr = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(ALT_DB_USER, ALT_DB_PASS, ALT_DB_HOST, ALT_DB_PORT, ALT_DB_NAME)
db = create_engine(connstr, pool_recycle=3600)

with db.connect() as con:

  json_files = [pos_json for pos_json in os.listdir(codebase+'/_maps') if pos_json.endswith('.json')]

  for j in json_files:
    maps.append(json.load(open(codebase+'/_maps/'+j)))

  query = text('INSERT INTO jobs (mapcount, maplist, repohash) VALUES (:mapcount, :maplist, :hash)')
  result = con.execute(query, mapcount=len(json_files), maplist=json.dumps(maps), hash=repohash)
  jobid = result.lastrowid
  for j in json_files:
    map = json.load(open(codebase+'/_maps/'+j))

    command = "../SpacemanDMM/target/debug/dmm-tools minimap -o ../renders --pngcrush {0}".format('_maps/'+map['map_path']+'/'+map['map_file'])

    print("Rendering {0}...".format(map['map_name']))
    query = text('INSERT INTO renders (job, mapname, mapfile) VALUES (:job, :mapname, :mapfile)')
    result = con.execute(query, job=jobid, mapname=map['map_name'], mapfile=map['map_file'])
    renderid = result.lastrowid
    print(command)
    call(command.split(), shell=False, cwd=codebase)

    tilecommand = "./tile.sh renders/{0}-1.png {1} 256 5".format(map['map_file'].replace('.dmm',''),map['map_name'].replace(' ',''))

    print("Tiling {0}...".format(map['map_name']))
    query = text('UPDATE renders SET ended = NOW() WHERE id = :renderid')
    con.execute(query, renderid=renderid)

    query = text('UPDATE jobs SET completed = completed+1 WHERE id = :jobid')
    con.execute(query, jobid=jobid)
    call(tilecommand.split(), shell=False)

  query = text('UPDATE jobs SET finished = NOW() WHERE id = :jobid')
  con.execute(query, jobid=jobid)