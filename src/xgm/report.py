# 项目：   新柜面统计
# 模块：   报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-05-07 08:03

from orange import Data, Path, hasher
from orange.xlsx import Book, Header, write_excel

from . import Xjdz, db

Headers = [
    Header("交易码", 10),
    Header("交易名称", 40),
    Header("交易组", 10),
    Header("交易组名", 22),
    Header("一级菜单", 20),
    Header("二级菜单", 25),
    Header("近一年交易量", 10, "number"),
    Header("类型", 10),
    Header("部门", 20),
    Header("中心", 30),
    Header("联系人", 15),
    Header("方案", 16),
    Header("计划需求完成时间", 10),
    Header("当前进度", 23),
    Header("备注", 45),
    Header("新交易", 50),
    Header("校验码", 10, hidden=True),
]


tongji_sql = """
select lxr,zx,
sum(iif((sfwc is null or sfwc ='0-尚未开始' or sfwc='' ),1,0)),       -- 未开始
sum(iif(sfwc in('1-已编写初稿','2-已提交需求/确认需规'),1,0)),       -- 已完成需求
sum(iif(sfwc in('3-已完成开发','4-已完成验收测试'),1,0)),       -- 开发中
sum(iif(sfwc = '5-已投产' ,1,0)),       -- 已完成需求
count(jym) as zs         -- 总数
from xmjh
where ywbm='运营管理部' and fa not in('1-下架交易','5-移出柜面系统')
group by zx,lxr
order by zs desc
"""

tongji_gzx_sql = """
select zx,
sum(iif((sfwc is null or sfwc ='0-尚未开始' or sfwc='' ),1,0)),       -- 未开始
sum(iif(sfwc in('1-已编写初稿','2-已提交需求/确认需规'),1,0)),       -- 已完成需求
sum(iif(sfwc in('3-已完成开发','4-已完成验收测试'),1,0)),       -- 开发中
sum(iif(sfwc = '5-已投产' ,1,0)),       -- 已完成需求
count(jym) as zs         -- 总数
from xmjh
where ywbm='运营管理部' and fa not in('1-下架交易','5-移出柜面系统')
group by zx
order by zs desc
"""

tongji_gbm_sql = """
select lx,
sum(iif(fa <> '1-下架交易' and(sfwc is null or sfwc ='0-尚未开始' or sfwc=''),1,0)),       -- 未开始
sum(iif(fa <> '1-下架交易' and sfwc in('1-已编写初稿','2-已提交需求/确认需规'),1,0)),       -- 已完成需求
sum(iif(fa <> '1-下架交易' and sfwc in('3-已完成开发','4-已完成验收测试'),1,0)),       -- 开发中
sum(iif(fa <> '1-下架交易' and sfwc = '5-已投产',1,0)),       -- 已完成需求
count(jym) as zs         -- 总数
from xmjh
where fa not in('1-下架交易','5-移出柜面系统')
group by lx
order by zs desc
"""


def rpt_work(book, rpt_date):
    """运营管理部需求完成情况表"""
    cur_tongji_ygb_sql = """
select a.zx,
sum(iif(ifnull(sfwc,'')in('0-尚未开始','') ,1,0)),       -- 未开始
sum(iif(sfwc in('1-已编写初稿','2-已提交需求/确认需规'),1,0)),       -- 已完成需求
sum(iif(sfwc in('3-已完成开发','4-已完成验收测试') ,1,0)),       -- 开发中
sum(iif(sfwc = '5-已投产' ,1,0)),       -- 已完成需求
count(jym) as zs,         -- 总数
b.zhrs,b.fhrs               -- 总行人数、分行人数
from xmjh a
left join ryb b on a.zx=b.zx
where ywbm='运营管理部' and fa not in('1-下架交易','5-移出柜面系统')
group by a.zx
order by zs desc
"""

    book.add_table(
        sheet="运营管理部需求完成表",
        data=db.fetch(cur_tongji_ygb_sql),
        total_row=True,
        columns=[
            Header("中心", 20, total_string="合计"),
            Header("未提交需求", 10, "number", total_function="sum"),
            Header("已完成需求", 10, "number", total_function="sum"),
            Header("开发中", 10, "number", total_function="sum"),
            Header("已投产", 10, "number", total_function="sum"),
            Header("总数", 10, "number", total_function="sum"),
            Header("总行人数", 10, "number", total_function="sum"),
            Header("分行人数", 10, "number", total_function="sum"),
            Header("投产完成率", 10, formula="=[已投产]/[总数]", format="percent"),
        ],
    )
    # 科技管理部编写需求完成情况
    # 科技管理部已完成所有需求初稿的编写工作，该报表不再需要。


def rpt_kaifa(book: Book):
    "统计开发完成情况"
    sql = (
        'select iif(ywbm="运营管理部",fa,iif(fa<>"1-下架交易","2-直接迁移","1-下架交易"))as xfa,sum(iif(ifnull(sfwc,"") in("","0-尚未开始"),1,0)), '
        "sum(iif(sfwc in('1-已编写初稿','2-已提交需求/确认需规'),1,0)), "
        "sum(iif(sfwc = '3-已完成开发' ,1,0)),"
        "sum(iif(sfwc = '4-已完成验收测试' ,1,0)),"
        "sum(iif(sfwc = '5-已投产' ,1,0)), "
        "count(jym) as zs  "
        "from xmjh "
        "where xfa not in('1-下架交易','5-移出柜面系统') "
        "group by xfa "
        "order by zs desc "
    )

    book.add_table(
        sheet="开发完成情况",
        data=db.fetch(sql),
        total_row=True,
        columns=[
            Header("方案", 19, total_string="合计"),
            Header("未提交需求", 12, "number", total_function="sum"),
            Header("待开发", 12, "number", total_function="sum"),
            Header("已开发", 12, "number", total_function="sum"),
            Header("已验收", 12, "number", total_function="sum"),
            Header("已投产", 12, "number", total_function="sum"),
            Header("总数", 12, "number", total_function="sum"),
            Header("投产完成率", 12, formula="=[已投产]/[总数]", format="percent"),
        ],
    )


def export_mxb(book: Book):
    """导出交易明细表"""
    # 计划表
    todo_sql = (
        "select * from xmjh where sfwc is null or not sfwc like '5%' order by jym"
    )
    # 完成表
    complete_sql = "select * from xmjh where sfwc like '5%' order by jym"
    # 总表
    total_sql = "select * from xmjh order by jym"

    for sheet, sql in zip(
        ["计划表", "完成表", "全量表"], [todo_sql, complete_sql, total_sql]
    ):
        data = tuple(Data(db.fetch(sql), hasher(-9, -8, -7, -6, -5, -4, -3, -2, -1)))
        if data:
            book.add_table(sheet=sheet, data=data, columns=Headers)


def export(path, rpt_date):
    """导出计划表数据"""
    with path.write_xlsx(force=True) as book:
        # rpt_work(book, rpt_date)
        book.add_table(
            sheet="统计表",
            name="Tongji",
            pos="A1",
            data=db.fetch(tongji_sql),
            total_row=True,
            columns=[
                Header("联系人", 12, total_string="合计"),
                Header("中心", 20),
                Header("未提交需求", 10, "number", total_function="sum"),
                Header("已完成需求", 10, "number", total_function="sum"),
                Header("开发中", 10, "number", total_function="sum"),
                Header("已投产", 10, "number", total_function="sum"),
                Header("总数", 10, "number", total_function="sum"),
                Header(
                    "投产完成率",
                    10,
                    formula="=[已投产]/[总数]",
                    total_function="Tongji[[#Totals],[已投产]]/Tongji[[#Totals],[总数]]",
                    format="percent",
                ),
            ],
        )

        book.add_table(
            sheet="统计表",
            pos="B31",
            name="gzx",
            total_row=True,
            data=db.fetch(tongji_gzx_sql),
            columns=[
                Header("中心", 20, total_string="合计"),
                Header("未提交需求", 10, "number", total_function="sum"),
                Header("已完成需求", 10, "number", total_function="sum"),
                Header("开发中", 10, "number", total_function="sum"),
                Header("已投产", 10, "number", total_function="sum"),
                Header("总数", 10, "number", total_function="sum"),
                Header(
                    "投产完成率",
                    10,
                    formula="=[已投产]/[总数]",
                    total_function="gzx[[#Totals],[已投产]]/gzx[[#Totals],[总数]]",
                    format="percent",
                ),
            ],
        )

        book.add_table(
            sheet="统计表",
            name="gbm",
            pos="B43",
            data=db.fetch(tongji_gbm_sql),
            total_row=True,
            columns=[
                Header("类型", 20, total_string="合计"),
                Header("未提交需求", 10, "number", total_function="sum"),
                Header("已完成需求", 10, "number", total_function="sum"),
                Header("开发中", 10, "number", total_function="sum"),
                Header("已投产", 10, "number", total_function="sum"),
                Header("总数", 10, "number", total_function="sum"),
                Header(
                    "投产完成率",
                    10,
                    formula="=[已投产]/[总数]",
                    total_function="gbm[[#Totals],[已投产]]/gbm[[#Totals],[总数]]",
                    format="percent",
                ),
            ],
        )
        # rpt_kaifa(book)
        export_kfjh(book)
        export_mxb(book)
        export_xjdz(book)
        print("更新文件成功！")


def rpt_xqqs():
    "生成需求明细缺失报告表"
    with write_excel(Path("E:/需求明细表缺失.xlsx")) as book:
        sql = 'select a.jym,a.jymc,a.lxr,a.sfwc from xmjh a left join xqmxb b on a.jym=b.jym where a.sfwc in("2-已提交需求/确认需规","3-已完成开发","5-已投产") and b.jym is null order by a.jym'
        book.add_table(
            sheet="需求明细缺失",
            data=db.fetch(sql),
            columns=[
                Header("交易码", 12),
                Header("交易名称", 45),
                Header("联系人", 16),
                Header("完成进度", 30),
            ],
        )
        print("导出需求缺失文件成功")


def export_xjdz(book):
    "导出新旧交易对照表"
    Xjdz.export(
        db,
        book=book,
        sheetname="投产交易一览表",
        sql="select * from xjdz order by jym,yjym",
    )
    print("导出文件成功")


kfjh_sql = """
select a.jym,a.jymc,a.jyz,a.jyzm,a.yjcd,a.ejcd,a.bs,a.lx,a.ywbm,a.zx,a.lxr,a.fa,
b.xqzt,b.kfzt,b.jhbb,b.kjfzr,b.kfzz,b.qdkf,b.hdkf,b.lckf,b.jcks,b.jcjs,b.ysks,b.ysjs
from xmjh a
left join kfjh b on a.jym=b.jym
where b.jym is not null
order by b.jhbb,a.jym
"""


def export_kfjh(book: Book):
    "导出开发计划表"
    book.add_table(
        sheet="开发计划",
        data=db.fetch(kfjh_sql),
        columns=[
            Header("交易码", 10),
            Header("交易名称", 40),
            Header("交易组", 10),
            Header("交易组名", 22),
            Header("一级菜单", 20),
            Header("二级菜单", 25),
            Header("近一年交易量", 10, "number"),
            Header("类型", 10),
            Header("部门", 20),
            Header("中心", 30),
            Header("联系人", 15),
            Header("方案", 16),
            Header("需求状态", 12),
            Header("开发状态", 12),
            Header("计划版本", 12),
            Header("开发负责人", 15),
            Header("开发组长", 15),
            Header("前端开发", 15),
            Header("后端开发", 15),
            Header("流程开发", 15),
            Header("集成测试开始", 15),
            Header("集成测试结束", 15),
            Header("验收测试开始", 15),
            Header("验收测试结束", 15),
        ],
    )
