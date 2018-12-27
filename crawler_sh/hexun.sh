#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/hexun_crawler/hexun_crawler
nohup scrapy crawl hexun_crawler 2>&1 &
