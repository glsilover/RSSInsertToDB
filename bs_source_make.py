import logging
import requests
from bs4 import BeautifulSoup
import lxml
# from selenium import webdriver
from public_method import construct_data


class BSSourceMake:
    def __init__(self, source, source_dict):
        self.source = source
        self.source_url = source_dict['url']
        self.domain = source_dict['domain']
        self.tags = source_dict['tags']
        self.folder = source_dict['folder']
        self.priority = source_dict['priority']
        self.article_data_list = []


    def deeplearning_ai(self):
        response = requests.get(self.source_url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        notice_items = soup.find_all('article')

        for item in notice_items:
            target_link = ''
            try:
                description = ''
                published_at = ''

                # 获取link
                links = item.find_all('a')
                for link in links:
                    if 'issue' in link.get('href'):
                        target_link = self.domain + link.get('href')

                divs = item.find_all('div')
                # 获取简介和时间
                if len(divs) >= 2:
                    # 获取第二个div下的所有div(第一个div是图片)
                    second_div_divs = divs[1].find_all('div')
                    # 打印每个div的内容
                    published_at = second_div_divs[0].text
                    description = second_div_divs[1].text

                content_dict = construct_data(
                    item.find('h2').text.strip(),
                    target_link,
                    description,
                    self.tags,
                    self.folder,
                    self.source,
                    published_at,
                    self.priority
                )
                self.article_data_list.append(content_dict)

            except Exception as e:
                logging.info(f"解析文章失败:{target_link} {e}")
                continue
        return self.article_data_list

    # def ali_product_news(self):
    #     # 预处理
    #     driver = webdriver.Chrome()
    #     driver.get(self.source_url)
    #     html = driver.page_source
    #     driver.quit()
    #     soup = BeautifulSoup(html, 'lxml')
    #     notice_items = soup.find_all('div', class_='product-show-content-item')
    #     for item in notice_items:
    #         target_link = ''
    #         try:
    #             description = item.find_all('div', class_='desc')[0].text.strip()
    #             published_at = item.find_all('div', class_='time')[0].text.strip()
    #             title = item.find_all('a', class_='ace-link ace-link-primary title')[0].text.strip()
    #             # 获取link
    #             links = item.find_all('a')
    #             for link in links:
    #                 if 'news/detail' in link.get('href'):
    #                     target_link = self.domain + link.get('href')
    #
    #             content_dict = construct_data(
    #                 title,
    #                 target_link,
    #                 description,
    #                 self.tags,
    #                 self.folder,
    #                 self.source,
    #                 published_at
    #             )
    #             self.article_data_list.append(content_dict)
    #
    #         except Exception as e:
    #             logging.info(f"解析文章失败:{target_link} {e}")
    #             continue
    #     return self.article_data_list
