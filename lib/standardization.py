"""
格式化城市区域
"""
from lib.region_block import city_dict, region_dict
from lib.log import LogHandler

log = LogHandler(__name__)


def standard_city(city_name):
    """

    :param city_name: 城市名称
    :return: 城市名称
    """
    for city_name_in_fangjia in city_dict.keys():
        for nick_name in city_dict[city_name_in_fangjia]:
            if nick_name in city_name:
                return True, city_name_in_fangjia
    log.error("城市无法标准化：{}".format(city_name))
    return False, city_name


def standard_block(city_name, region_name):
    """

    :param city_name: 城市名称
    :param region_name: 区域
    :return: 区域
    """
    result, city_name = standard_city(city_name)
    if result:
        for region_list in region_dict[city_name].values():
            for region in region_list:
                if region in region_name:
                    return True, region
    else:
        log.error("城市无法标准化：{},无法格式话区域".format(city_name))
        return False, city_name

# if __name__ == '__main__':
#     a, b = standard_city('  宁波  ')
#     print(b)
#     a, b = standard_block('武汉   江岸区', '    武汉   江岸区')
#     print(b)
