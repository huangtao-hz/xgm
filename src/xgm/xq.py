# 项目：   对需求明细表进行分析
# 模块：   需求明细表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-06-09 14:10

import pandas as pd
from orange import Path, datetime


def convdate(s):
    try:
        s = datetime(s) % "%F"
    except Exception:
        s = None
    return s


def xqmxfx(month: str, week: int = 0):
    "对需求明细表进行分析和统计，形成报告"
    # 读取需求明细表
    path = Path("~/Documents/当前工作/20250331新柜面简报").find(
        "附件*数智综合运营系统业务需求明细表*.xlsx"
    )
    if not path:
        print("文件未找到！")
        return
    lines = []
    xqmxb = pd.read_excel(
        str(path),
        sheet_name="需求明细表",
        converters={
            "实际提交": convdate,
            "需求评审": convdate,
            "提交开发日期": convdate,
        },
    )
    xqmxb["提交部门"].replace(
        ["赞同科技", "科技管理部"], ["科技部门", "科技部门"], inplace=True
    )
    for col in ("实际提交", "需求评审", "提交开发日期"):
        xqmxb[col] = pd.to_datetime(
            xqmxb[col], errors="coerce"
        )  # 把文本格式修改成日期格式
    if week:
        xqfx = xqmxb[xqmxb["实际提交"].dt.isocalendar().week == week]
    xqs, qt, jys = xqfx.agg(
        {"需求名称": "nunique", "提交部门": "count", "交易码": "count"}
    )
    lines.append(
        "".join(
            [
                f"共提交{xqs}份业务需求",
                f"，其中公共或优化类需求{qt - jys}份" if qt - jys else "",
                f"，涉及原柜面交易{jys}个，",
            ]
        )
    )

    lines.append("其中：")
    a = xqfx.groupby("提交部门")
    for bm, sj in a:
        if bm == "运营管理部":
            lines.append(f"{bm}完成{sj['交易码'].count()}个交易的迁移需求，")
        else:
            ...
    lines[-1] = lines[-1][:-1] + "。"
    print("".join(lines))
