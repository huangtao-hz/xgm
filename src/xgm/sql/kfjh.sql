select a.jym,a.jymc,a.lx,a.ywbm,a.zx,a.lxr,a.fa,
b.xqzt,b.kfzt,b.jhbb,b.kjfzr,b.kfzz,b.qdkf,b.hdkf,b.lckf,b.jcks,b.jcjs,b.ysks,b.ysjs
from xmjh a
left join kfjh b on a.jym=b.jym
where a.sfwc<>'5-已投产'
and a.fa not in ('1-下架交易','5-移出柜面系统')
order by b.jhbb,a.jym
