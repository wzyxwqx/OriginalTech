#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/jrj_crawler/jrj_crawler/
nohup scrapy crawl jrj_crawler 2>&1 &

