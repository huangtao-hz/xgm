# 项目：   数智综合运营系统项目管理
# 模块：   报告模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-06-07 15:06

from orange import R, datetime, suppress

from . import db

YZX = dict(zip("严重,一般,轻微,建议".split(","), range(4)))
ZT = dict(
    zip(
        "待分析,待业务需求,已计划版本,持续跟踪,已解决,已关闭".split(","),
        range(6),
    )
)


def yzx_sort(value1: str, value2: str) -> int:
    return YZX.get(value1, 9) - YZX.get(value2, 9)


def zt_sort(value1: str, value2: str) -> int:
    return ZT.get(value1, 9) - ZT.get(value2, 9)


db.create_collation("yzx_order", yzx_sort)
db.create_collation("zt_order", zt_sort)


@suppress
def xqfx(bgq: str, query: str) -> None:
    "生成需求分析报告"
    lines = ["一、需求完成情况\n"]
    sql = (
        'select count(distinct a.xqmc),ifnull(sum(iif(a.jym="",0,1)),0),ifnull(sum(iif(a.jym="",1,0)),0), '
        'sum(iif(a.jym<>"" and bxbm<>"运营管理部",1,0)),'
        'sum(iif(a.jym<>"" and bxbm="运营管理部",1,0)),'
        'sum(iif(a.jym<>"" and bxbm<>"运营管理部" and b.lx="本部门" ,1,0)),'  # 本部门
        'sum(iif(a.jym<>"" and bxbm<>"运营管理部" and b.lx="其他部门" ,1,0)),'  # 其他部门
        'sum(iif(a.jym<>"" and bxbm<>"运营管理部" and b.lx="分行需求" ,1,0)) '  # 其他部门
        "from xqmxb a "
        "left join xmjh b on a.jym=b.jym "
        "where "
    )
    sql += query.format(field="tjrq")
    xqs = db.fetchone(sql)
    lines.append(
        f"本周，共收到业务需求{xqs[0]}份（涵盖{xqs[1]}个存量交易"
        + (f"和{xqs[2]}份优化需求" if xqs[2] else "")
        + "）,"
    )
    ygbjy = xqs[4] - xqs[2]
    lines.append(
        f"科技部门编写的直接迁移需求{xqs[3]}份（其中运营管理部交易{xqs[5]}份，其他部门交易{xqs[6]}份，分行交易{xqs[7]}份），"
        f"运营管理部编写的业务需求{xqs[4]}份（涵盖{ygbjy}个存量交易和{xqs[2]}份优化需求）。"
    )

    sql = """
select count(jym),
sum(iif(lx='本部门',1,0)),
sum(iif(lx='本部门' and fa<>'2-直接迁移',1,0)),
sum(iif(lx='其他部门',1,0)),
sum(iif(lx='分行需求',1,0))
from xmjh
where fa not in('1-下架交易') and sfwc='0-尚未开始'
    """
    a = [x if x else 0 for x in db.fetchone(sql)]
    kjbx = a[0] - a[2]
    ygbzq = a[1] - a[2]
    if a[0]:
        lines.append(
            "\n截至报告期，尚有{0}个交易未提交需求，其中：运营管理部负责编写的交易需求{2}个（总交易数{1}个）；科技管理部负责编写的交易需求{5}个，"
            "运营管理部直接迁移类需求 {6}个，其他部门交易{3}个，分行交易{4}个，详见附件1。".format(
                *a, kjbx, ygbzq
            )
        )
    print("".join(lines))


@suppress
def wtgzbg(bgq: str, query: str) -> None:
    "生成问题跟踪报告"
    lines = ["二、生产问题跟踪情况\n"]
    sql = (
        "select yzx,count(wtms)from wtgzb where "
        + query.format(field="tcrq")
        + " group by yzx order by yzx collate yzx_order"
    )
    sj = dict(db.fetch(sql))
    zs = sum(sj.values())
    lines.append(f"本周，共收集{zs}个问题，其中：")
    lines.append(
        "，".join(
            "{}问题{}个（{:.2f}%）".format(*a, a[1] * 100 / zs)
            for a in sj.items()
        )
    )
    lines.append("。\n")

    sql = "select zt,count(wtms)from wtgzb group by zt order by zt collate zt_order"
    sj = dict(db.fetch(sql))
    zs = sum(sj.values())
    lines.append(f"截至报告期，项目组累计收集问题{zs}个，其中：")
    lines.append(
        "，".join(
            "{}问题{}个（{:.2f}%）".format(*a, a[1] * 100 / zs)
            for a in sj.items()
        )
    )
    lines.append("。")
    print("".join(lines))


def rpt_xqqk(rptperiod: str) -> None:
    "生成月度或周报"
    bgq, query = "", ""
    if R / r"\d{4}\-\d{2}" == rptperiod:
        bgq = "{0}年{1}月".format(*rptperiod.split("-"))
        query = f'{{field}} like "{rptperiod}%"'
    elif R / r"\d{4}\-\d{2}\-\d{2}" == rptperiod:
        week = datetime(rptperiod).format("%W")
        bgq = f"第{week}周"
        query = f'strftime("%W",{{field}})="{week}"'
    else:
        print("Error: 日期格式错误，应为：YYYY-mm 月报；YYYY-mm--dd 周报")
        return
    print("报告期：", bgq)
    xqfx(bgq, query)
    wtgzbg(bgq, query)
