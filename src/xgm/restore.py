# 项目：   新柜面计划执行情况
# 模块：   主程序
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-09-17 18:43

import contextlib
import tarfile

from orange import Path, datetime, extract, suppress
from orange.excel import read_excel
from orange.sqlite import Connection

from xgm import Kfjh, Wtgzb, Xjdz


def conv_xjdz(row:list)->list:
    '新旧对照表数据转换'
    row=list(row)
    if isinstance(row[0],(float,int)):
        row[0]=f'{int(row[0]):05d}'
    if isinstance(row[2],(float,int)):
        row[2]=f'{int(row[2]):04d}'
    if isinstance(row[4],(float,int)):
        row[4]=datetime(row[4]).strftime("%Y-%m")
    return row

@suppress
def load_xjdz(db:Connection,contents,path:Path,ver:str):
    "从迁移计划表中导入新旧交易对照表"
    data = read_excel(file_contents=contents,sheets='投产交易一览表',skiprows=1,converter=conv_xjdz)
    with db:
        db.lcheck('xjdz',path,path.mtime,ver)
        Xjdz.load(
            db,
            method="replace",
            data=data,
            path=path,
            loadcheck=True,
            clear=True,
            print_result=True,
        )

def conv_jhb(row: list) -> list:
    '转换计划表'
    row=list(row)[:16]
    if isinstance(row[0],(float,int)):
        row[0]=f'{int(row[0]):04d}'
    if isinstance(row[12], (float, int)):
        with contextlib.suppress(Exception):
            row[12] = datetime(row[12]).strftime("%Y-%m")
    return row

@suppress
def load_jhb(db:Connection,contents,path:Path,ver:str):
    '导入计划表'
    data = read_excel(file_contents=contents,sheets='全量表',skiprows=1,converter=conv_jhb)
    with db:
        db.lcheck('xmjh',path,path.mtime,ver)
        db.load("xmjh", 16, data=data, clear=True, method="insert", print_result=True)

@suppress
def load_kfjh(db:Connection,contents,path:Path,ver:str):
    "从迁移计划表中导入开发计划"
    def conv(row: list) -> list:
        return [row[0], *row[12:24]]
    data = read_excel(file_contents=contents,sheets='开发计划',skiprows=1,converter=conv)
    with db:
        db.lcheck('kfjh',path,path.mtime,ver)
        Kfjh.load(
            db,
            method="replace",
            data=data,
            path=path,
            loadcheck=True,
            clear=False,
            print_result=True,
        )

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
def load_scwtb(db:Connection,contents,path:Path,ver:str):
    print('导入生产问题跟踪表')
    data = read_excel(file_contents=contents,sheets='问题清单',skiprows=1,converter=conv_scwtb)
    with db:
        db.lcheck('wtgzb',path,path.mtime,ver)
        Wtgzb.load(
            db,
            data=data,
            loadcheck=True,
            clear=True,
            print_result=True,
        )


def restore(db:Connection):
    '从备份数据中导入数据'
    path=Path('~/Downloads').find('新柜面简报*.tgz')
    if not path:
        print('未在 ~/Downloads 文件夹下发现 新柜面简报YYYYMMDD.tgz 文件')
        return

    print('处理文件：',path.name)
    with tarfile.open(path,'r:gz')as f:
        ver=extract(path.pname,r'\d{8}')
        print('版本：',ver)
        members=f.getmembers()
        for member in members:
            if '新柜面存量交易迁移计划' in member.name:
                contents=f.extractfile(member)
                if contents:
                    print('导入计划表')
                    bytes=contents.read()
                    load_jhb(db,bytes,path,ver)
                    print('导入新旧交易对照表')
                    load_xjdz(db,bytes,path,ver)
                    print('导入开发计划表')
                    load_kfjh(db,bytes,path,ver)
            elif '数智综合运营系统问题跟踪表' in member.name:
                print('数智综合运营系统问题跟踪表')
                contents=f.extractfile(member)
                if contents:
                    bytes=contents.read()
                    load_scwtb(db,bytes,path,ver)
