from orange.sqlite import Connection


def update_ytc(db: Connection):
    "根据新旧交易对照表更新已完成的交易"
    sql = "select a.jym,a.jymc,a.sfwc,b.jym,b.jymc,b.tcrq from xmjh a join xjdz b on a.jym=b.yjym where a.sfwc not like '5%' and b.tcrq <date('now')"
    data = db.fetch(sql)
    if data:
        print("以下交易已有新旧交易对照表，其状态不是已完成：")
        print(data, sep="\n")
        if input("是否更新状态为已完成，Y or N?") in "Yy":
            with db:
                i = 0
                for i, (jym, *other) in enumerate(data):
                    db.execute("update xmjh set sfwc='5-已投产' where jym=?", [jym])
                print("更新数量：", i)
