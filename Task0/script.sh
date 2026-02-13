#!/bin/bash; 
while true; do ts=$(date +%s); start=$(date +%s%3N); code=$(curl -o /dev/null -s -w "%{http_code}" https://google.com); end=$(date +%s%3N); rt=$((end-start)); echo "$ts $code $rt"; sleep 1; done
