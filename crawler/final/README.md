# 期末作品

项目要求：

1. 针对使用 AJAX 或 JavaScript 动态加载内容的网站（如电商平台商品列表），使用 Selenium 或 Puppeteer 模拟浏览器行为抓取数据。
2. 实现分页功能，自动翻页并抓取每一页的商品信息（如名称、价格、销量等）。
3. 将抓取的数据存储到数据库中（如 SQLite 或 MySQL），并设计合理的数据库表结构。
4. 编写简单的 Web 界面（使用 Flask 或 Django），展示数据库中存储的商品信息。

加分项：

1. 引入多线程或异步 IO（如 asyncio）加速数据抓取过程。
2. 使用代理 IP 池避免 IP 被封禁。
3. 对抓取的数据进行简单的去重和清洗。

---

网络安全搜索引擎（Vue + FastAPI + ？）

目标：

- 安全内参：https://www.secrss.com/
- 先知社区：https://xz.aliyun.com/
- FreeBuf：https://www.freebuf.com/
- 奇安信攻防社区：https://forum.butian.net/

步骤：

- 爬取数据，获取网页文档集合，数据库存储 uid, url, title, 网页原文档存储到 {uid}.html
- 文档分词，中文 jieba 分词，英文 nltk 分词，存储到数据库
- 倒排索引 -> TF-IDF 矩阵, TfidfVectorizer 对象
- 获取搜索词，分词 -> TF-IDF 向量化 -> 余弦相似度计算 -> 返回结果

---

Ref:

https://blog.csdn.net/qq_35993946/article/details/88087827 - 使用 Python 实现简单的搜索引擎，完整源码
https://blog.csdn.net/zz_dd_yy/article/details/51926305 - 相似度算法之余弦相似度
https://github.com/fxsjy/jieba - fxsjy/jieba: 结巴中文分词
https://blog.csdn.net/codejas/article/details/80356544 - Python 入门：jieba 库的使用
https://blog.csdn.net/qq_36560894/article/details/115408613 - 谈谈距离度量方式：欧氏距离与余弦距离

---
