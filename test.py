# import requests
# from lib.mongo import Mongo
#
#
# m = Mongo('127.0.0.1', 27018)
# coll = m.connect['dianping']['shop_info']
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
# }
#
#
# def scan():
#     for i in range(100000, 500000000):
#         print(i)
#         url_id = 'https://m.dianping.com/shop/' + str(i)
#         response = requests.get(url_id, headers=headers)
#         html = response.text
#         if 'name="Description' in html:
#             coll.insert_one({'_id': str(i)})
#             print(response.status_code, '插入一条数据')
#
#
# if __name__ == '__main__':
#     scan()

from lib.rabbitmq import Rabbit

r = Rabbit('127.0.0.1', 5673)
channel = r.get_channel()


def init_rabbit():
    id_list = []
    for i in range(100000, 500000000):
        if i % 100 == 0:
            channel.queue_declare(queue='dianping')
            channel.basic_publish(exchange='',
                                  routing_key='dianping',
                                  body=str(id_list))
            print(id_list)
            id_list = []
        else:
            id_list.append(i)


if __name__ == '__main__':
    init_rabbit()
