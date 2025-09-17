# 项目：   新柜面项目
# 模块：   AB3 崩溃次数报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-07-25 08:24

from orange.sqlite import Connection
from orange.xlsx import Header, Path, write_excel

from . import Bkjl

BkHeaders = (
    Header("日期", width=12, total_string="合计"),
    Header("机构数", width=12, format="number"),
    Header("设备数", width=12, format="number"),
    Header("崩溃次数", width=12, format="number", total_function="sum"),
)


def bk_rpt(db: Connection):
    "生成近一周内 ab3 崩溃次数报告"
    rqs = [
        x[0] for x in db.fetch("select distinct rq from bkjl order by rq desc limit 7")
    ]
    path = Path(f"~/Downloads/近一周内系统崩溃次数统计表({rqs[0]}) .xlsx")
    with write_excel(path) as book:
        # 生成汇总表
        book.add_table(
            total_row=True,
            sheet="汇总",
            columns=BkHeaders,
            data=db.fetch(
                "select rq,count(distinct jgh),count(distinct ip),sum(zdcs)from bkjl group by rq order by rq desc limit 7"
            ),
        )
        book.add_table(
            sheet="崩溃次数超过2的设备",
            columns=[
                Header("分行", 31),
                Header("机构号", 13),
                Header("IP地址", 15),
                Header("操作系统", 45),
                Header("天数", 10),
                Header("总次数", 10),
            ],
            data=db.fetch(
                "select fh,jgh,ip,czxt,count(rq)as ts,sum(zdcs)as cs from bkjl "
                "where rq between ? and ? group by ip having ts>1 order by ts desc,cs desc",
                [rqs[-1], rqs[0]],
            ),
        )
        for rq in rqs:
            Bkjl.export(
                db,
                book=book,
                sheetname=rq,
                sql=f'select * from bkjl where rq="{rq}" order by zdcs desc ',
            )
        print(path, "导出成功")
