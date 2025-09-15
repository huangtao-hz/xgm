# 项目：   日常使用工具
# 模块：   新柜面 bug 统计
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2024-10-30 12:22
# 修订：2024-11-06 11:04 新增统计文字

from itertools import chain

from orange import Path, arg, command, datetime, now, slicer, suppress

from . import db


@suppress
@db.tran
def load():
    """
    导入系统生成测试系统导出的缺陷清单，文件应放在“下载”目录。文件名的格式应为：DP2024958644柜面系统焕新升级项目+4位数字日期。
    param:无
    returns:无
    """
    path = Path("~/Downloads").find("DP2024958644柜面系统焕新升级项目*.xlsx")
    if path:
        print(path.name)
        data = path.read_sheet(
            slicer(14),
            sheet=0,
            start_row=1,
        )
        db.lcheck("wtqd", path, path.mtime)
        print("导入 bug 清单：", end="")
        db.load(
            "wtqd", 14, data, method="insert", clear=True, print_result=True
        )
    else:
        print("下载目录未发现相关文件")


Report = """科技管理部测试中心测试人员、分行业务测试人员继续进行测试。共提交测试缺陷%d个，其中：致命缺陷%d个，严重缺陷%d个，一般缺陷%d个，轻微缺陷%d个，均已指派给对应开发人员。
当日共关闭测试缺陷%d个，其中：致命缺陷%d个，严重缺陷%d个，一般缺陷%d个，轻微缺陷%d个。
截至当日，未关闭的缺陷%d个，其中：致命缺陷%d个，严重缺陷%d个，一般缺陷%d个，轻微缺陷%d个；超过3天以上未关闭的缺陷%d个。其中公司方已解决缺陷%d个，待业务复测后关闭。"""

# 当日提出问题统计
tc_sql = """select count(bh),sum(iif(yzcd='致命',1,0)),sum(iif(yzcd='严重',1,0)),sum(iif(yzcd='一般',1,0)),sum(iif(yzcd='轻微',1,0))
from wtqd
where cjrq between ? and ?
"""

# 当日解决问题统计
jj_sql = """select count(bh),sum(iif(yzcd='致命',1,0)),sum(iif(yzcd='严重',1,0)),sum(iif(yzcd='一般',1,0)),sum(iif(yzcd='轻微',1,0))
from wtqd
where gbrq between ? and ?
"""

# 汇总统计
hz_sql = """select count(bh),       -- 缺陷总数
sum(iif(yzcd='致命',1,0)),sum(iif(yzcd='严重',1,0)),sum(iif(yzcd='一般',1,0)),sum(iif(yzcd='轻微',1,0)), -- 致命缺陷、严重缺陷、一般缺陷
sum(iif(cjrq<=date(?,"-3 days") ,1,0)),     -- 3天以上未关闭的缺陷
sum(iif(zt='已解决',1,0))                   -- 待复测的缺陷
from wtqd
where zt<>'已关闭' and cjrq<=?
"""


def tongji(curdate: str = ""):
    """
    在屏幕上输出统计数据
    params:无
    returns:无
    """
    if not curdate:
        "默认查询当日数据"
        cur_date = now()
        if cur_date.weekday() == 0:
            cur_date = cur_date - 2
        curdate = (cur_date - 1) % "%F"
    rq = [curdate, curdate]
    if datetime(curdate).weekday() == 4:
        "报告日期如为周五，则统计周末数据"
        rq[-1] = (datetime(curdate) + 2) % "%F"

    print("报告日期：", curdate)
    print("统计区间：", *rq)
    db.printf(
        "累计提交缺陷：{:,d}个", "select count(*)from wtqd", print_rows=False
    )
    data = chain(
        *map(lambda sql: db.fetchone(sql, rq), [tc_sql, jj_sql, hz_sql])
    )
    data = tuple(0 if x is None else x for x in data)
    print(Report % tuple(data))


@command(allow_empty=True, description="新柜面测试问题统计分析")
@arg("rptdate", nargs="?", help="报告日期")
def main(**options):
    load()
    tongji(options.get("rptdate"))


if __name__ == "__main__":
    main()
