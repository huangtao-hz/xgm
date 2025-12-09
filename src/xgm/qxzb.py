from orange import Path
from . import Home
from .util import load_file


def conv(row):
    if row[0]:
        return row


def load_qxzb():
    path = Path(Home).find("*缺陷指标详情*.*")
    if path:
        print("处理文件：", path.name)
        load_file(str(path), "xgm", "loader/qx_qxzb.toml", converter=conv)
