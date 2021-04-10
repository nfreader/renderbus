#!/bin/bash

maps=`find "$1" -type f -name '*.dmm' | tr '\n' ' '`
echo /Users/farleyn/Developer/SpacemanDMM/target/release/dmm-tools --env ~/Developer/tgstation/tgstation.dme minimap -o ~/Desktop/renders $maps

/Users/farleyn/Developer/SpacemanDMM/target/release/dmm-tools --env ~/Developer/tgstation/tgstation.dme minimap -o ~/Desktop/renders "$maps"