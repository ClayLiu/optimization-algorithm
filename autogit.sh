#!/bin/sh
mode=`git diff`
if [ -n mode ];then
  echo 'ok'
else
  echo 'no'
fi
