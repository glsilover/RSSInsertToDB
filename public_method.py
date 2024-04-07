import mysql.connector
from mysql.connector import Error
from dateutil import parser
from dateutil.tz import gettz
import lxml
from datetime import datetime, timezone, timedelta
import logging
from bs4 import BeautifulSoup

china_timezone = timezone(timedelta(hours=8))


def china_time_converter(*args):
    """
    自定义时间转换器，将UTC时间转换为北京时间。
    """
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(china_timezone).timetuple()


def connect_to_database(internet=False):
    if internet:
        host = ''
        port = 48176
    else:
        host = ''
        port = 3306
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database='rss',
            user='admin',
            password='',
            ssl_disabled=True
        )
        if connection.is_connected():
            return connection
    except Error as e:
        logging.info(f"Error connecting to MySQL: {e}")
        return None


def clean_html(html_content):
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, "lxml")
    # 获取无格式的文本
    text = soup.get_text()
    return text


def convert_to_cst(datetime_str):
    # 解析日期字符串
    try:
        dt = parser.parse(datetime_str)
        # 转换到中国标准时间（UTC+8）
        cst_dt = dt.astimezone(gettz("Asia/Shanghai"))
        return cst_dt
    except Exception as e:
        return datetime.now()


def construct_data(title, link, description, tags, folder, source, published_at, source_priority):
    # 构造SQL插入语句，包括所有字段
    content_dict = {
        'title': clean_html(title),
        'link': link,
        'description': clean_html(description),
        'tags': ",".join(tags) if tags else 'default',
        'folder': folder,
        'source': source,
        'published_at': convert_to_cst(clean_html(published_at)),
        'priority': source_priority,
    }
    return content_dict
