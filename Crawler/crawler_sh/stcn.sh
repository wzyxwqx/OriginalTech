#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/stcn_crawler/stcn_crawler/
nohup scrapy crawl stcn_crawler 2>&1 &

