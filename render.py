#!/usr/bin/env python
#
# render.py - Renders maps

import os, sys, zipfile, re, json, getopt
import subprocess
from subprocess import call
import argparse
from datetime import datetime
from shutil import copyfile

parser = argparse.ArgumentParser(description='Render some maps')
parser.add_argument('codebase', metavar='N', type=str, nargs=1,
                    help='Path to the tgstation code repository')
parser.add_argument('spacemandmm', metavar='N', type=str, nargs=1,
                    help='Path to dmm-tools')
parser.add_argument('out_dir', metavar='N', type=str, nargs=1,
                    help='Path to output directory')
args = parser.parse_args()

codebase = args.codebase[0]
spacemandmm = args.spacemandmm[0]
out_dir = args.out_dir[0]
dme = f"{codebase}/tgstation.dme"
maps_dir = f"{codebase}/_maps"


print(codebase)
print(dme)
print(maps_dir)
print(spacemandmm)

# print("Updating codebase repository...")
# call("git pull".split(), shell=False, cwd=codebase)
# repohash = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],stdout=subprocess.PIPE, cwd=codebase)
# repohash = repohash.stdout.decode('UTF-8')
startTime = datetime.now()
maps = []
renderlist = []

json_files = [pos_json for pos_json in os.listdir(maps_dir) if pos_json.endswith('.json')]

for j in json_files:
    maps.append(json.load(open(codebase+'/_maps/'+j)))

for m in maps:
	if isinstance(m['map_file'], list):
		for f in m['map_file']:
			renderlist.append(f"{maps_dir}/{m['map_path']}/{f}")
	else:
		renderlist.append(f"{maps_dir}/{m['map_path']}/{m['map_file']}")

rendercmd = f"{spacemandmm} --env {dme} minimap -o {out_dir} {' '.join(renderlist)}"
call(rendercmd.split(), shell=False, cwd=codebase)
with open(f"{out_dir}/maps.json", 'w') as mapjson:
    json.dump(maps, mapjson)
print(datetime.now() - startTime)