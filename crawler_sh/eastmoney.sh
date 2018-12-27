#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/eastmoney_crawler/eastmoney_crawler
nohup scrapy crawl eastmoney_crawler 2>&1 &
