# 项目：   新柜面系统
# 模块：   数据表机构
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-01-07 10:38

from orange import Path
from orange.config import Config
from orange.sqlite import connect
from orange.table import Column, Table

conf = Config("xmjh")
db = connect(conf.get("database", "xgm2025-03"))
home = conf.get("Home", "~/Documents/当前工作/20250331新柜面简报")
Home = Path(home)


class Wtgzb(Table):
    """问题跟踪表"""

    tablename = "wtgzb"
    xh = Column("序号", _type="text", width=10)
    jygn = Column("交易/功能", width=25)
    wtms = Column("问题描述", width=45)
    yzx = Column("严重性", width=8)
    tcrq = Column("提出日期", width=12)
    tcjg = Column("提出机构", width=20)
    yhfx = Column("原因分析", width=30)
    zt = Column("状态", width=10)
    wtfl = Column("问题分类", width=15)
    clfa = Column("处理方案", width=35)
    jhbb = Column("计划版本", width=12)
    zrr = Column("责任人", width=15)
    bz = Column("备注", width=25)


class FhYwzj(Table):
    """分支行业务专家清单"""

    tablename = "ywzj"
    fh = Column("分行", _type="text", width=20)
    xm = Column("姓名", _type="text", width=12)
    gh = Column("工号", _type="text", width=10)
    kh = Column("卡号", _type="text", width=10)
    xb = Column("性别", _type="text", width=10)
    cdsj = Column("抽调时间", _type="text", width=15)
    bdsj = Column("报到时间", _type="text", width=15)
    lxr = Column("总行联系人", _type="text", width=12)
    gznr = Column("工作内容", _type="text", width=12)


class Bkjl(Table):
    """新柜面系统 AB3 崩次数统计表"""

    tablename = "bkjl"
    rq = Column("日期", _type="text", width=11, is_pk=True)
    jgh = Column("机构号", _type="text", width=13)
    fh = Column("所属分行", _type="text", width=35)
    ip = Column("IP地址", _type="text", width=13, is_pk=True)
    czxt = Column("操作系统", _type="text", width=45)
    nc = Column("内存", _type="text", width=15)
    zdcs = Column("AB3中断次数", _type="text", width=10)


class Kfjh(Table):
    """新柜面科技开发计划"""

    tablename = "kfjh"
    jym = Column("交易码", _type="text", width=11, is_pk=True)
    xqzt = Column("需求状态", _type="text", width=12)
    kfzt = Column("开发状态", _type="text", width=12)
    jhbb = Column("计划版本", _type="text", width=12)
    kjfzr = Column("行方负责人", _type="text", width=15)
    kfzz = Column("技术组长", _type="text", width=15)
    qdkf = Column("前端开发", _type="text", width=15)
    hdkf = Column("后端开发", _type="text", width=15)
    lckf = Column("流程开发", _type="text", width=15)
    jcks = Column("集成测试开始时间", _type="text", width=12)
    jcjs = Column("集成测试结束时间", _type="text", width=12)
    ysks = Column("验收测试开始时间", _type="text", width=12)
    ysjs = Column("验收测试结束时间", _type="text", width=12)


class Xjdz(Table):
    """新旧交易对照表"""

    tablename = "xjdz"
    jym = Column("交易码", _type="text", width=12)
    jymc = Column("交易码称", _type="text", width=45)
    yjym = Column("原交易码", _type="text", width=12)
    yjymc = Column("原交易码称", _type="text", width=45)
    tcrq = Column("投产日期", _type="text", width=12)
    zs = Column("状态", _type="text", width=12)
    bz = Column("备注", _type="text", width=30)
