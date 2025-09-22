# 项目：   数智综合运营系统项目管理
# 模块：   展示交易信息
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-09-05 09:54
from orange.sqlite import Connection


def show_jy(db: Connection, jym: str):
    fa, zt, jhbb = db.fetchone(
        "select fa,sfwc,jhbb from xmjh a left join kfjh b on a.jym=b.jym where a.jym=?",
        [jym],
    )
    if fa[0] in "15":
        header = "交易码,交易名称,交易笔数,类型,业务部门,中心,业务联系人,改造方案"
        sql = "select a.jym,a.jymc,a.bs,a.lx,a.ywbm,a.zx,a.lxr,a.fa from xmjh a left join kfjh b on a.jym=b.jym where a.jym=?"
        db.print_row(header, sql, [jym])
    elif zt[0] in "5":
        header = "交易码,交易名称,交易笔数,类型,业务部门,中心,业务联系人,改造方案,状态,对应新交易,投产日期"
        sql = """select a.jym,a.jymc,a.bs,a.lx,a.ywbm,a.zx,a.lxr,a.fa,a.sfwc,printf('%s-%s',c.jym,c.jymc),c.tcrq
        from xmjh a
        left join xjdz c on a.jym=c.yjym
        where a.jym=?"""
        db.print_row(header, sql, [jym])
    elif jhbb is None:
        header = "交易码,交易名称,交易笔数,类型,业务部门,中心,业务联系人,改造方案,状态"
        sql = 'select a.jym,a.jymc,a.bs,a.lx,a.ywbm,a.zx,a.lxr,a.fa,printf("%s（未制定计划）",a.sfwc) from xmjh a where a.jym=?'
        db.print_row(header, sql, [jym])
    else:
        header = "交易码,交易名称,交易笔数,类型,业务部门,中心,业务联系人,改造方案,计划版本,技术经理,开发组长"
        sql = "select a.jym,a.jymc,a.bs,a.lx,a.ywbm,a.zx,a.lxr,a.fa,b.jhbb,b.kjfzr,b.kfzz from xmjh a left join kfjh b on a.jym=b.jym where a.jym=?"
        db.print_row(header, sql, [jym])


def show_xjy(db: Connection, jym: str):
    header = "交易码,交易名称,投产日期,备注"
    db.print_row(
        header, "select distinct jym,jymc,tcrq,bz from xjdz where jym=? ", [jym]
    )
    print("        ---    对应老交易清单     ---")
    sql = "select a.jym,a.jymc,a.ywbm,a.zx,a.lxr from xmjh a left join xjdz b on a.jym=b.yjym where b.jym=?"
    db.printf("{:4s}  {:30s}  {:12s}  {:10s}  {:8s}", sql, [jym])


def show_tc_tj(db: Connection):
    "统计各版本投产交易数量"
    header = "投产日期   交易数量 迁移交易数量 新交易数量    占比（%）"
    sql = """select tcrq,count(distinct jym),sum(iif(yjym<>"",1,0)),sum(iif(yjym="",1,0)),
    sum(iif(yjym<>"",1,0))*100.0/(select count(jym)from xmjh where fa not in ("1-下架交易","5-移出柜面系统"))
    from xjdz
    where tcrq<=date('now')
    group by tcrq
    union
    -- 显示合计数据
    select '合计',count(distinct jym),sum(iif(yjym<>"",1,0)),sum(iif(yjym="",1,0)),
    sum(iif(yjym<>"",1,0))*100.0/(select count(jym)from xmjh where fa not in ("1-下架交易","5-移出柜面系统"))
    from xjdz
    where tcrq<=date('now')
    """
    format = "{:10s}  {:8,d}  {:8,d}  {:8,d}        {:5.2f}%"
    print(header)
    db.printf(format, sql, print_rows=True)
