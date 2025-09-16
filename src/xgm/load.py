# 项目：   新柜面项目计划
# 模块：   导入文本文件
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-01-07 10:30

import contextlib
from typing import Iterable

from orange import (
    Data,
    Path,
    R,
    converter,
    datetime,
    hashfilter,
    slicer,
    suppress,
)
from orange.table import convdata

from . import Bkjl, FhYwzj, Kfjh, Wtgzb, Xjdz, conf, db

home = Path(conf.get("Home", "~/Documents/当前工作/20250331新柜面简报"))


@converter
def conv_jhb(row: list) -> list:
    if isinstance(row[12], (float, int)):
        with contextlib.suppress(Exception):
            row[12] = datetime(row[12]).strftime("%Y-%m")
    return row


@db.tran
def load_jhb(path: Path):
    def read() -> Iterable:
        for sheetname in ("全量表", "计划表", "完成表"):  # '完成表'):
            try:
                data = path.read_sheet(sheet=sheetname, start_row=1)
                data = Data(
                    data,
                    conv_jhb,
                    hashfilter(-10, -9, -8, -7, -6, -5, -4, -3, -2, -1),
                    slicer(16),
                )
                yield from data
            except Exception as e:
                print(e)

    data = tuple(read())
    db.load("xmjh", 16, data=data, clear=False, method="replace", print_result=True)
    r = db.execute('delete  from xmjh where jym like "____.0" ')
    if r.rowcount > 0:
        print("删除数量:", r.rowcount)


def load_xjdz2(path: Path):
    "从迁移计划表中导入新旧交易对照表"
    data = path.read_sheet(sheet="投产交易一览表", start_row=1)
    Xjdz.load(
        db,
        method="replace",
        data=data,
        path=path,
        loadcheck=True,
        clear=True,
        print_result=True,
    )


@db.tran
def load_kfjh2(path: Path):
    "从迁移计划表中导入开发计划"

    def conv(row: list) -> list:
        return [row[0], *row[12:24]]

    data = path.read_sheet(sheet="开发计划", start_row=1)
    data = convdata(data, conv)

    Kfjh.load(
        db,
        method="replace",
        data=data,
        path=path,
        loadcheck=True,
        clear=False,
        print_result=True,
    )


@converter
def conv_xqmx(row: list) -> list:
    row = list(row)
    row[0] = f"{int(row[0]):04d}" if isinstance(row[0], (int, float)) else row[0]
    for i in range(7, 10):
        with contextlib.suppress(Exception):
            row[i] = datetime(row[i]) % "%F"

    return row[:11]


@suppress
@db.tran
def load_xqmxb():
    # 导入需求明细表
    path = home.find("附件*数智综合运营系统业务需求明细表*.xlsx")
    if path:
        print("处理文件：", path.name)
        data = path.read_sheet(conv_xqmx, sheet="需求明细表", start_row=1)
        db.lcheck("xqmxb", path.name, path.mtime)
        db.load("xqmxb", 11, data=data, clear=True, print_result=True)


def conv_scwtb(row: list) -> list:
    "生产问题表转换程序"
    row = list(row[:15])
    row[0] = int(row[0])
    for i in (4, 10):
        try:
            row[i] = datetime(row[i]) % "%F"
        except Exception:
            row[i] = None
    return row


@suppress
@db.tran
def load_scwtb():
    # 导入生产问题跟踪表
    path = home.find("*数智综合运营系统问题跟踪表*.xlsx")
    if path:
        print("处理文件：", path.name)
        # data = path.read_sheet(conv_xqmx, sheet='需求明细表', start_row=1)
        # db.lcheck('xqmxb', path.name, path.mtime)
        # db.load('xqmxb', 11, data=data, clear=True, print_result=True)
        data = path.read_sheet(sheet="问题清单", start_row=1)
        Wtgzb.load(
            db,
            data=convdata(data, conv_scwtb),
            loadcheck=True,
            clear=True,
            print_result=True,
        )


def conv_ywzj(row: list) -> list:
    "业务专家清单转换程序"
    row = list(row)
    for i in (6, 7):
        try:
            row[i] = datetime(row[i]) % "%F"
        except Exception:
            row[i] = None
    return row[1:10]


@suppress
@db.tran
def load_ywzj():
    # 导入业务专家清单
    path = home.find("抽调建设数智综合运营系统分支行业务专家清单*.xls*")
    if path:
        print("处理文件：", path.name)
        data = path.read_sheet(sheet="Sheet1", start_row=3)
        FhYwzj.load(
            db,
            data=data,
            convfunc=conv_ywzj,
            loadcheck=True,
            clear=True,
            print_result=True,
        )


@suppress
@db.tran
def load_bkcs(path: Path):
    """导入系统崩溃次数表"""
    print("处理文件:", path.name)
    rq = path.pname[-10:]

    def conv_bkjl(row):
        "系统崩溃次数转换程序"
        row[-1] = int(row[-1])
        return rq, *row

    if R / r"\d{4}\-\d{2}\-\d{2}" == rq:
        data = path.read_sheet(sheet="Sheet1", start_row=1)
        Bkjl.load(
            db,
            method="replace",
            data=data,
            convfunc=conv_bkjl,
            path=path,
            loadcheck=True,
            clear=False,
            print_result=True,
        )


YUE = R / r"\d{1,2}"


def conv_kfjh(row):
    "转换开发计划"
    if isinstance(row[0], (int, float)):
        row[0] = f"{int(row[0]):04d}"
    yuefen = int(YUE.extract(row[3], 0))
    if yuefen <= 3:
        row[3] = f"2026-{yuefen:02d}"
    else:
        row[3] = f"2025-{yuefen:02d}"
    return *row[:9], None, None, None, None


@suppress
@db.tran
def load_kfjh():
    "导入开发计划"
    path = home.find("新柜面交易开发计划*.xlsx")
    if path:
        print("处理文件:", path.name)
        data = path.read_sheet(sheet=0, start_row=1)
        data = convdata(data, conv_kfjh)
        Kfjh.load(
            db,
            method="replace",
            data=data,
            path=path,
            loadcheck=True,
            clear=False,
            print_result=True,
        )


@suppress
@db.tran
def load_xjdz():
    "导入新旧交易对照表"
    path = home.find("新旧交易对照表*.xlsx")
    if not path:
        print("未发现投产交易清单，忽略")
        return
    print("处理文件:", path.name)
    oldrow = []

    def conv_xjdz(row):
        nonlocal oldrow
        row[0] = row[0] or oldrow[0]
        row[1] = row[1] or oldrow[1]

        if isinstance(row[0], (float, int)):
            row[0] = f"{int(row[0]):05d}"
        if isinstance(row[2], (float, int)):
            row[2] = f"{int(row[2]):04d}"
        row[4] = datetime(row[4]) % "%F"
        oldrow = row
        return row

    data = convdata(path.read_sheet(sheet=0, start_row=1), conv_xjdz)
    Xjdz.load(
        db,
        method="replace",
        data=data,
        path=path,
        loadcheck=True,
        clear=True,
        print_result=True,
    )


def load_all():
    "导入所有数据"
    load_scwtb()  # 问题跟踪表
    load_xqmxb()  # 需求明细表
    load_ywzj()  # 业务专家表
    load_kfjh()  # 导入开发计划
    for path in Path("~/Downloads").glob("崩溃记录表*.xlsx"):
        load_bkcs(Path(path))
