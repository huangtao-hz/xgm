# 项目：   新柜面系统
# 模块：   数据表机构
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-01-07 10:38

from orange.config import Config
from orange.sqlite import connect
from orange.table import Column, Table

conf = Config("xmjh")
db = connect(conf.get("database", "xgm2025-03"))


db.executescript("""
--Bug编号	Bug标题	严重程度	重现步骤	Bug状态	激活次数	由谁创建	创建日期	指派给	解决者	解决方案	解决日期	由谁关闭	关闭日期
create table if not exists wtqd(
    bh      text    primary key, -- Bug编号
    bt      text,   --  Bug标题
    yzcd    text,   --	严重程度
    cxbz    text,   --	重现步骤
    zt      text,   --	Bug状态
    jhcs    int,    --  激活次数
    cjr     text,   --	由谁创建
    cjrq    text,   --	创建日期
    zp      text,   --	指派给
    jjr     text,   --	解决者
    jjfa    text,   --	解决方案
    jjrq    text,   --	解决日期
    gbr     text,   --  由谁关闭
    gbrq    text    --	关闭日期
);

create table if not exists xmjh(
    jym     text    primary key,    -- 交易码
    jymc    text,   --  交易名称
    jyz     text,   -- 交易组
    jyzm    text,   -- 交易组名
    yjcd    text,   -- 一级菜单
    ejcd    text,   -- 二级菜单
    bs      int,    -- 交易笔数
    lx      text,   -- 类型：0-本部门，1-总行部门，2-分行特色
    ywbm    text,   -- 业务部门
    zx      text,   -- 中心
    lxr     text,   -- 业务联系人
    fa      text,   -- 改造方案  0-下架交易，1-直接迁移，2-改造迁移，3-重新设计,4-移出柜面系统
    pc      text,   -- 批次
    sfwc    text,   -- 是否完成
    bz      text,   -- 备注信息
    xjym    text    -- 新交易码
);

-- 建立索引
create index if not exists xmjh_ywbm on xmjh(ywbm);
create index if not exists xmjh_zx on xmjh(zx);
create index if not exists xmjh_lxr on xmjh(lxr);
create index if not exists xmjh_sfwc on xmjh(sfwc);
create index if not exists xmjh_fa on xmjh(fa);

-- 需求明细表
create table if not exists xqmxb(
    jym     text,   --交易码
    jymc    text,   --交易名称
    bxbm    text,   --提交部门
    bxr     text,   --提交人
    xqmc    text,   --需求名称
    zt      text,   --状态
    jhyf    text,   --应提交月份
    tjrq    text,   --实际提交
    psrq    text,   --需求评审
    zstjrq  text,   --提交开发日期
    bz      text    --备注
);

-- 建立索引
create index if not exists xqmxb_jym on xqmxb(jym);
create index if not exists xqmxb_bxbm on xqmxb(bxbm);
create index if not exists xqmxb_tjrq on xqmxb(tjrq);
create index if not exists xqmxb_psrq on xqmxb(psrq);
create index if not exists xqmxb_zstjrq on xqmxb(zstjrq);


create view if not exists ryb as
select d.zx,count(d.lxr) as zhrs,c.fhrs
from
(select distinct zx,lxr from xmjh where ywbm='运营管理部') d left join
(select b.zx,count(a.lxr) as fhrs
from ywzj a join (select distinct zx,lxr from xmjh where ywbm='运营管理部') b on a.lxr=b.lxr
where a.bdsj is not null and a.bdsj<=date('now')
group by b.zx) c on d.zx=c.zx
where d.zx <>""
group by d.zx;
""")


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


# 批量生成数据库表
for k, v in globals().copy().items():
    if isinstance(v, type) and issubclass(v, Table) and v is not Table:
        v.create_table(db)
