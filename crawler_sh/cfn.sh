#!/bin/sh
source ~/.bashrc
cd /root/originaltech/crawler/cfn_crawler/cfn_crawler
nohup scrapy crawl cfn_crawler 2>&1 &
