from pkgutil import get_data
from typing import Callable, List, Optional

from orange import Path, suppress
from orange.excel import read_excel
from toml import loads

from . import db


def load(
    excel_file: str = "",
    tablename: str = "",
    sheets: Optional[str] = "",
    use_cols: str = "",
    skip_rows: int = 0,
    check: bool = True,
    ver: str = "",
    converter: Optional[Callable[[List], Optional[List]]] = None,
    **kw,
):
    if data := read_excel(
        excel_file,
        sheets=sheets,
        usecols=use_cols,
        skiprows=skip_rows,
        converter=converter,
    ):
        if check:
            db.lcheck(tablename, excel_file, Path(excel_file).mtime, ver=ver)
        db.load(data=data, table=tablename, **kw, print_result=True)


@suppress
def load_file(
    excel_file: str,
    pkg: str,
    toml_file: str,
    ver: str = "",
    converter: Optional[Callable[[List], Optional[List]]] = None,
):
    if pkg_data := get_data(pkg, toml_file):
        kwargs = loads(pkg_data.decode())
        with db:
            load(excel_file, converter=converter, ver=ver, **kwargs)
