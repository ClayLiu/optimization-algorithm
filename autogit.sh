#!/bin/sh
git diff > /dev/null
echo $?
if [ -n mode ];then
  echo 'ok'
else
  echo 'no'
fi
