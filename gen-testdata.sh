#!/bin/sh

while  python ./gen_urllog.py >> url.log
do
  sleep 5
  echo "next"
done

