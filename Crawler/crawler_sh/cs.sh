#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/cs_crawler/cs_crawler/
nohup scrapy crawl cs_crawler 2>&1 &
