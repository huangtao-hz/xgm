from pkgutil import get_data

from orange import Path, extract

from . import Home, db
from .util import load_file


def export_xmjh(path: Path):
    db.export_excel(
        "xgm",
        path,
        "tables/jh_gbmtj.toml",
        "tables/jh_gzxtj.toml",
        "tables/jh_ywtj.toml",
        "tables/jh_kfjhtj.toml",
        "tables/jh_gzxkfjh.toml",
        "tables/jh_kfjhb.toml",
        "tables/jh_xmjhb.toml",
        "tables/jh_tcjyb.toml",
        "tables/jh_bbap.toml",
    )
    print(f"导出文件 {path.name} 成功！")


def load_xmjh(path: Path):
    "导入版本明细表"
    if path:
        print("处理文件：", path)

        file = str(path)
        ver = extract(file, r"\d{8}")
        ver = "-".join([ver[:4], ver[4:6], ver[6:]])
        print("导入开发计划", end="")
        load_file(file, "xgm", "loader/jh_kfjh.toml")
        print("导入项目计划", end="")
        load_file(file, "xgm", "loader/jh_xmjh.toml")
        print("导入投产交易一览表", end="")
        load_file(file, "xgm", "loader/jh_xjdzb.toml")
        print("导入版本安排", end="")
        load_file(file, "xgm", "loader/jh_bbap.toml")


def update_xmjh():
    if path := Home.find("附件*新柜面存量交易迁移计划*.xlsx"):
        load_xmjh(path)
        update_zt()
        export_xmjh(path)


@db.tran
def exec(file):
    if data := get_data("xgm", file):
        r = db.execute(data.decode())
        print(f"更新{r.rowcount:,d}行数据")


def update_ytc():
    "根据新旧交易对照表更新已完成的交易"
    sql = """
    select a.jym,a.jymc,a.sfwc,b.jym,b.jymc,b.tcrq
    from xmjh a join xjdz b on a.jym=b.yjym
    where a.sfwc not like '5%' and b.tcrq <date('now') and b.tcrq<>''
    """
    data = db.fetch(sql)
    if data:
        print("以下交易已有新旧交易对照表，其状态不是已完成：")
        print(*data, sep="\n")
        if input("是否更新状态为已完成，Y or N?") in "Yy":
            with db:
                sql = """update xmjh
                        set sfwc='5-已投产'
                        from xjdz
                        where sfwc<>'5-已投产' and xmjh.jym=xjdz.yjym and tcrq<date('now') and tcrq<>'' """
                r = db.execute(sql)
                print("更新数量：", r.rowcount)


def update_zt():
    "根据当期进度更新计划总表"
    print("根据验收明细表更新开发状态:", end="")
    exec("query/update_kfjihua.sql")
    print("根据计划版本更新开发计划时间：", end="")
    exec("query/update_kfjhsj.sql")
    print("根据验收条目更新完成状态：", end="")
    exec("query/update_xmjh.sql")
    print("根据新旧交易对照表更新对应新交易：", end="")
    exec("query/update_xmjh_xjy.sql")
    update_ytc()
