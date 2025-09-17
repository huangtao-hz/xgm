# 项目：   新柜面计划执行情况
# 模块：   主程序
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-04-03 09:39
# 修订：2025-09-05 14:45 新增导入开发计划表和新旧交易对照表的功能

from orange import Path, R, arg, command, datetime

from . import conf, db
from .baogao import rpt_xqqk
from .bkbg import bk_rpt
from .load import (
    load_all,
    load_jhb,
    load_kfjh2,
    load_xjdz2,
)
from .report import export
from .show import show_jy, show_tc_tj, show_xjy

home = conf.get("Home", "~/Documents/当前工作/20250331新柜面简报")
Home = Path(home)


@command(prog="xmjh", description="新柜面规划处理程序")
@arg("-u", "--update", action="store_true", help="更新计划进度")
@arg("-t", "--touchan", action="store_true", help="统计投产交易清单")
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
@arg('-R','--restore',action='store_true',help='从备份数据中导入')
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
        path = Home.find("附件*新柜面存量交易迁移计划*.xlsx")
        if path:
            rpt_date = datetime(path.pname[-8:]) % "%F"
            print("报告日期：", rpt_date)
            print("处理文件：", path.name)
            load_jhb(path)
            print("导入开发计划")
            load_kfjh2(path)
            print("导入新旧交易对照表")
            load_xjdz2(path)
            # load_xqmxb()
            export(path, rpt_date)
    jym = options.get("jym")
    if jym:
        if R / r"\d{4}" == jym:
            show_jy(db, jym)

        elif R / r"\d{5}" == jym:
            show_xjy(db, jym)

    if options.get("touchan"):
        show_tc_tj(db)
    if sql := options.get("sql"):
        db.print(sql)

    if options.get("load"):
        "导入数据"
        load_all()
    if options.get('restore'):
        from xgm.restore import restore
        restore(db)
    rptperiod = options.get("rptperiod")
    if rptperiod and rptperiod != "noset":
        # load_xqmxb()
        rpt_xqqk(rptperiod)

    if options.get("bengkui"):
        bk_rpt(db)


if __name__ == "__main__":
    main()
