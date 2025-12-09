# 项目：   新柜面计划执行情况
# 模块：   主程序
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-04-03 09:39
# 修订：2025-09-05 14:45 新增导入开发计划表和新旧交易对照表的功能

from orange import R, arg, command


from . import db
from .baogao import rpt_xqqk
from .bbmx import update_bbmx


# from .load import load_all, load_jhb, load_kfjh2, load_xjdz2, update_jhb
# from .report import export
from .show import show_jh, show_jy, show_tc_tj, show_xjy
from .xmjh import update_xmjh
from .qxzb import load_qxzb


@command(prog="xmjh", description="新柜面规划处理程序")
@arg("-u", "--update", action="store_true", help="更新计划进度")
@arg("-t", "--touchan", action="store_true", help="统计投产交易清单")
@arg("-j", "--jihua", action="store_true", help="统计计划安排")
@arg(
    "-r",
    "--report",
    nargs="?",
    dest="rptperiod",
    default="noset",
    help="生成报告",
)
@arg("-l", "--load", action="store_true", help="导入数据")
@arg("-b", "--bengkui", action="store_true", help="崩溃次数")
@arg("jym", nargs="?", help="查询交易情况")
@arg("-R", "--restore", action="store_true", help="从备份数据中导入")
@arg(
    "-q",
    "--qurey",
    nargs="?",
    dest="sql",
    metavar="sql",
    help="执行 sql 查询语句",
)
def main(**options):
    if options.get("update"):
        load_qxzb()
        update_bbmx()
        update_xmjh()

    jym = options.get("jym")
    if jym:
        if R / r"\d{4}" == jym:
            show_jy(db, jym)

        elif R / r"\d{5}" == jym:
            show_xjy(db, jym)
    if options.get("jihua"):
        show_jh(db)
    if options.get("touchan"):
        show_tc_tj(db)
    if sql := options.get("sql"):
        db.print(sql)

    if options.get("restore"):
        pass
    rptperiod = options.get("rptperiod")
    if rptperiod and rptperiod != "noset":
        # load_xqmxb()
        rpt_xqqk(rptperiod)

    if options.get("test"):
        pass


if __name__ == "__main__":
    main()
