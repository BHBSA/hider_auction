from source.rmfysszc import Rmfysszc
from source.jingdong import Jingdong
from source.ali import Ali
from source.gongpaiwang import Gongpaiwang
from source.jiapai import Jiapai

# ----
from chengjiwen.laipaiya import Laipaiya
from chengjiwen.shjiapai import Shjiapai
from chengjiwen.zhupaiwang import Zhupaiwang
# ----
from jijunyu.chinesesfpm import ChineseFPM

from source.qdspaimaizhongxin import Qingdaopaimai

from multiprocessing import Process

if __name__ == '__main__':
    jiapai = Jiapai()
    rmfysszc = Rmfysszc()
    jingdong = Jingdong()
    ali = Ali()
    gongpaiwang = Gongpaiwang()
    laipaiya = Laipaiya()
    shjiapai = Shjiapai()
    zhupaiwang = Zhupaiwang()
    chineseFPM = ChineseFPM()
    qingdaopaimai = Qingdaopaimai()

    Process(target=jiapai.start_crawler).start()
    Process(target=rmfysszc.start_crawler).start()
    Process(target=jingdong.start_crawler).start()
    Process(target=ali.start_crawler).start()
    Process(target=gongpaiwang.start_crawler).start()
    Process(target=laipaiya.start_crawler).start()
    Process(target=shjiapai.start_crawler).start()
    Process(target=zhupaiwang.start_crawler).start()
    Process(target=chineseFPM.start_crawler).start()
    Process(target=qingdaopaimai.start_crawler).start()
