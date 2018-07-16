"""
字段
"""
import datetime
import yaml
from lib.log import LogHandler
from lib.mongo import Mongo

log = LogHandler(__name__)

setting = yaml.load(open('config.yaml'))
client = Mongo(host=setting['mongo']['host'], port=setting['mongo']['port'], user_name=setting['mongo']['user_name'],
               password=setting['mongo']['password']).connect
coll = client[setting['mongo']['db']][setting['mongo']['collection']]


def check_auction(source, auction_id):
    return coll.find_one({'source': source, 'auction_id': str(auction_id)})


def serialization_info(info):
    """
    :param info:
    :return: data:
    """
    return {key: value for key, value in vars(info).items()}


class Auction:
    def __init__(self, source, auction_type, auction_name=None, start_auction_price=None, assess_value=None,
                 earnest_money=None,
                 announcement_date=None, auction_level=None, court=None, contacts=None, phone_number=None,
                 build_type=None, info=None, auction_id=None, auction_time=None, area=None, floor=None, province=None,
                 city=None, region=None, start_time=None, source_html=None, html_type=None):
        self.auction_name = auction_name  # 拍卖物品名称
        self.start_auction_price = start_auction_price  # 起拍价(元)
        self.assess_value = assess_value  # 评估值(元)
        self.earnest_money = earnest_money  # 保证金(元)
        self.announcement_date = announcement_date  # 公告日期(格式化)
        self.auction_level = auction_level  # 拍卖阶段
        self.court = court  # 法院
        self.contacts = contacts  # 联系人
        self.phone_number = phone_number  # 联系电话
        self.build_type = build_type  # 房产\住宅用房
        self.info = info  # 房屋信息
        self.source = source  # 网站来源
        self.auction_time = auction_time  # 拍卖时间： 拍卖开始时间，拍卖结束时间，流拍时间，成交时间(格式化)
        self.auction_id = str(auction_id)  # 拍卖物品id
        self.area = area  # 面积
        self.floor = floor  # 楼层
        self.auction_type = auction_type  # 拍卖物类型：房产，土地，小电车
        self.province = province  # 省
        self.city = city  # 市
        self.region = region  # 区域
        self.start_time = start_time  # 开始时间
        self.html_type = html_type  # 网站上的type
        self.source_html = source_html  # 原网页

    def insert_db(self):
        data = serialization_info(self)
        data['crawler_time'] = datetime.datetime.now()
        coll.insert_one(data)
        log.info('插入数据={}'.format(data))


if __name__ == '__main__':
    if check_auction(source='chinesesfpm', auction_id=2009):
        print('yes')
    else:
        print('no')
