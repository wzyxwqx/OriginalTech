#! /bin/bash
. /etc/profile
. ~/.bash_profile
cd /root/originaltech/crawler/cs_crawler/cs_crawler/
nohup scrapy crawl cs_crawler 2>&1 &
