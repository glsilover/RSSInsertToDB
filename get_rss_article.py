import mysql.connector
import feedparser
import logging
from bs_source_make import BSSourceMake
from public_method import connect_to_database, construct_data


class AllInOneArticle:
    def __init__(self, source, config):
        self.source = source
        self.config = config
        self.content_list = []

    def get_article(self):
        source_url = self.config[self.source]['url']
        source_type = self.config[self.source]['type']
        source_tags = self.config[self.source]['tags']
        source_folder = self.config[self.source]['folder']
        source_priority = self.config[self.source]['priority']
        logging.info(f"--------------------------------------------------")
        logging.info(f"开始解析RSS订阅: {source_url}")

        if source_type == 'rss':
            feed = feedparser.parse(source_url)
            logging.info(f"共找到{len(feed.entries)}篇文章。\n")

            for entry in feed.entries:
                try:
                    content_dict = construct_data(
                        entry.get('title', '无标题'),
                        entry.get('link', '未知链接'),
                        entry.get('summary', '无描述'),
                        source_tags,
                        source_folder,
                        self.source,
                        entry.get('published', '未知时间'),
                        source_priority

                    )
                    self.content_list.append(content_dict)
                except Exception as e:
                    logging.info(f"解析文章失败：{e}")
                    continue
            return

        elif source_type == 'web':
            source_instance = BSSourceMake(self.source, self.config[self.source])
            method_to_call = getattr(source_instance, self.source)  # 获取example_method方法
            self.content_list = method_to_call()
            return

    def insert_db(self):
        connection = connect_to_database()
        if connection is not None:
            cursor = connection.cursor()
            for content in self.content_list:
                try:
                    # 检查是否存在相同title的文章
                    check_query = "SELECT 1 FROM rss_articles WHERE title = %s"
                    cursor.execute(check_query, (content['title'],))
                    if cursor.fetchone():
                        # 如果找到了，说明已存在相同title的文章，跳过插入
                        logging.info(f"【Skipping】 Article '{content['title']}' already exists, skipping.")
                        continue

                    # 构造SQL插入语句，包括所有字段
                    insert_query = """
                    INSERT INTO rss_articles (title, link, description, tags, folder, source, published_at, pushed, priority) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE title=VALUES(title)
                    """
                    # 从article_content字典中提取字段值
                    title = content['title']
                    link = content['link']
                    description = content['description']
                    tags = content['tags']  # 假设tags是列表形式，转换为逗号分隔的字符串
                    folder = content['folder']
                    source = content['source']  # 假设source字段从类属性获取或其他逻辑
                    published_at = content['published_at']  # 确保published_at是datetime对象
                    pushed = False
                    priority = content['priority']

                    # 执行SQL语句
                    cursor.execute(insert_query, (title, link, description, tags, folder, source, published_at, pushed, priority))
                    connection.commit()
                    logging.info(f"【successfully】 Article '{title}' inserted successfully.")
                except mysql.connector.Error as e:
                    logging.info(f"【Failed】 Failed to insert article '{content['title']}'. MySQL Error: {e}")
                    continue  # 即使发生错误也继续尝试插入下一篇文章
            cursor.close()
            connection.close()
