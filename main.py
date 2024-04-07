import yaml
import logging
from get_rss_article import AllInOneArticle
from datetime import datetime, timezone, timedelta
from public_method import china_time_converter
import sys

docker_path = '/app/rss/'

with open(f'{docker_path}config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 设置时区
china_timezone = timezone(timedelta(hours=8))
timestamp = datetime.now(china_timezone).strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f"{docker_path}docker_log_rss_insert_db_{timestamp}.txt"

# 配置日志
logging.Formatter.converter = china_time_converter

logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    # 获取RSS内容，将RSS内容插入到数据库
    logging.info("【任务开始】 开始处理RSS订阅")

    for source in config['Source_List']:
        rss_insert = AllInOneArticle(source, config)
        rss_insert.get_article()
        rss_insert.insert_db()

    logging.info("\n\n\n\n\n【任务结束】 全部处理完成\n")
