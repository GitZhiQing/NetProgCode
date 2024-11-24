import requests
from bs4 import BeautifulSoup

# https://forum.butian.net/Rss

"""
<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title>奇安信攻防社区</title>
<link>forum.butian.net</link>
<description>description</description>
<item>
<guid>https://forum.butian.net/share/3899</guid>
<title>从rust堆看堆块伪造</title>
<description>本文章详细分析了强网杯S8的chat_with_me这道题，从rust堆看堆块伪造，最后getshell</description>
<source>subject</source>
<pubDate>2024-11-22 10:00:02</pubDate>
</item>
"""

url = "https://forum.butian.net/Rss"

response = requests.get(url)

soup = BeautifulSoup(response.text, "xml")

print(soup.find_all("item")[0].guid.string.split("/")[-1])
