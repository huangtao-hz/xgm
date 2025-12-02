# 项目：   新柜面系统
# 模块：   数据表机构
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2025-01-07 10:38

from orange import Path
from orange.config import Config
from orange.sqlite import connect

conf = Config("xmjh")
db = connect(conf.get("database", "xgm2025-03"))
home = conf.get("Home", "~/Documents/当前工作/20250331新柜面简报")
Home = Path(home)
db.executefile("xgm", "query/db.sql")
