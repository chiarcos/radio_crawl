#!/bin/bash

# remove duplicate mp3 files (based on streamripper numbering conventions, no deep checks ;)

# split at \n only
OIFS="$IFS"
IFS=$'\n'

type='mp3'

for dir in $*; do
  files=`find $dir | egrep '\([0-9]+\)\.'$type'$' `;
  if echo $files | grep $type >& /dev/null; then
    len=`echo $files | sed s/'\.'$type/'\n'/g | wc -l`
    echo found $len duplicate *.$type files in $dir, remove them? '[Y/n]'
    read -n 1 x
    if echo $x | grep '^[yY]*$' >&/dev/null; then
      for file in $files; do
        rm $file;
      done;
    fi;
  fi;
done;
