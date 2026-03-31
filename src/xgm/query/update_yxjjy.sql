-- 新增生产上已下架的交易
insert into xjjy
select a.jym,"1-直接下架",null
from xmjh a
left join jym c on a.jym=trim(c.jym)
left join xjjy d on a.jym=d.jym
where c.jym is null and d.jym is null
