#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/nbd_crawler/nbd_crawler
nohup scrapy crawl nbd_crawler 2>&1 &
