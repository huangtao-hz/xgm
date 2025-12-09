from typing import List, Optional

from orange import Path, extract

from . import Home, db
from .util import load_file


def export_bbmx(path: Path):
    "导出版本明细表"
    db.export_excel(
        "xgm",
        path,
        "tables/bb_kjtj.toml",
        "tables/bb_ywrytj.toml",
        "tables/bb_ywtj.toml",
        "tables/bb_qxzb.toml",
        "tables/bb_qxzbry.toml",
        "tables/bb_ystm.toml",
        "tables/bb_xjdzb.toml",
        "tables/bb_fgb.toml",
        "tables/bb_xmryb.toml",
    )
    print("导出文件：", path.name, "完成")


def load_bbmx(path: Path):
    "导入版本明细表"
    if path:
        print("处理文件：", path)

        file = str(path)
        ver = extract(file, r"\d{8}")
        ver = "-".join([ver[:4], ver[4:6], ver[6:]])

        print("导入分工表", end="")
        load_file(file, "xgm", "loader/bb_fgb.toml", ver=ver)
        print("导入交易对照表", end="")
        load_file(file, "xgm", "loader/bb_jydzb.toml", ver=ver)
        print("导入项目人员表", end="")
        load_file(file, "xgm", "loader/bb_xmryb.toml", ver=ver)
        print("导入验收条目表", end="")

        def conv_ystm(row: List) -> Optional[List]:
            return [ver, *row]

        load_file(file, "xgm", "loader/bb_ystm.toml", ver=ver, converter=conv_ystm)


def update_bbmx():
    "更新版本明细"
    if path := Home.find("*数智综合运营系统*版本条目明细.xlsx"):
        load_bbmx(path)
        export_bbmx(path)
