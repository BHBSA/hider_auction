import requests
from auction import Auction
from lib.log import LogHandler
from lib.mongo import Mongo
from lxml import etree
import datetime
import yaml
import re
import math
from sql_mysql import inquire, TypeAuction

setting = yaml.load(open('config.yaml'))
client = Mongo(host=setting['mongo']['host'], port=setting['mongo']['port'], ).connect
coll = client[setting['mongo']['db']][setting['mongo']['collection']]

source = 'jingdong'
log = LogHandler(__name__)
type_list = inquire(TypeAuction, source)
s = requests.session()


class Jingdong:
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
        }
        self.count = 0

    def start_crawler(self):
        for type_num in type_list:
            page_num = self.get_page(type_num.code)
            for page in range(1, int(page_num) + 1):
                url = 'http://auction.jd.com/getJudicatureList.html?page=' + str(
                    page) + '&limit=40&childrenCateId=' + type_num.code
                try:
                    response = s.get(url, headers=self.headers)
                    html = response.json()
                    try:
                        for info in html['ls']:
                            auction = Auction(source=source, auction_type=type_num.auction_type)
                            auction.html_type = type_num.html_type
                            auction.auction_name = info['title']  # 商品名
                            auction.assess_value = info['assessmentPrice']  # 评估值
                            try:
                                auction.province = info['province']  # 省
                                auction.city = info['city']  # 城市
                            except Exception as e:
                                auction.province = None
                                auction.city = None
                            auction.auction_time = datetime.datetime.fromtimestamp(int(info['startTime']) / 1000)  # 评估值
                            auction.earnest_money = info['currentPrice']  # 保证金
                            auction.auction_id = str(info['id'])  # 商品id
                            is_exist = coll.find_one({'auction_id': str(info['id']), 'source': source})
                            if is_exist:
                                log.info('id已存在，id="{}"'.format(str(info['id'])))
                                continue
                            self.get_detail(str(info['id']), auction)
                    except Exception as e:
                        log.error('解析错误，url="{}"'.format(url))
                except Exception as e:
                    log.error('请求错误，url="{}"'.format(url))

    def get_detail(self, id_, auction):
        info_list = []
        detail_url = 'http://paimai.jd.com/' + str(id_)
        response = s.get(detail_url, headers=self.headers)
        html = response.text
        start_auction_price = re.search('[起变][拍卖]价：.*?<em.*?>&yen;(.*?)</em>', html, re.S | re.M).group(1)
        auction.start_auction_price = float(start_auction_price.replace(' ', '').replace(',', ''))
        vendorId = re.search('id="vendorId" value="(.*?)"', html, re.S | re.M).group(1)
        auction.court = self.get_court(vendorId)  # 法院
        auction.contacts, auction.phone_number = self.get_contacts(id_)  # 联系人，联系电话
        tree = etree.HTML(html)
        info_list.append(tree.xpath('string(//div[@id="addition-desc"])'))
        info_list.append(tree.xpath('string(//div[@id="record-list"])'))
        auction.info = info_list
        auction.insert_db()

    def get_court(self, vendorId):
        sourt_url = 'http://paimai.jd.com/json/current/queryVendorInfo.html?vendorId=' + vendorId
        response = s.get(sourt_url, headers=self.headers)
        html = response.json()
        return html['shopName']

    def get_contacts(self, id_):
        url_ = 'http://mpaimai.jd.com/json/mobile/getProductbasicInfo.html?paimaiId=' + str(id_)
        headers_ = {
            'Referer': "http://mpaimai.jd.com/json/mobile/toProductLocation.html?paimaiId=" + str(id_),
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
        }

        response = s.get(url_, headers=headers_,allow_redirects=False)
        html = response.json()
        try:
            consultName = html['consultName']
            consultTel = html['consultTel']
        except Exception as e:
            consultName = None
            consultTel = None
        return consultName, consultTel

    def get_page(self, type_num):
        url_page = 'http://auction.jd.com/getJudicatureList.html?page=1&limit=40&_=1531121669367&childrenCateId=' + str(
            type_num)
        response = s.get(url_page, headers=self.headers)
        number = response.json()['total']
        page = math.ceil(int(number) / 40)
        return page
