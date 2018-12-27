#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/fin_crawler/fin_crawler
nohup scrapy crawl fin_crawler 2>&1 &
