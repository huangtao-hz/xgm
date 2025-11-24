from orange import Path, extract

from . import db
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
    if path := Path("~/Downloads").find("附件*新柜面存量交易迁移计划*.xlsx"):
        load_xmjh(path)
        export_xmjh(path)
