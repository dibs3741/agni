with
ctetotnotional as (
select
   asofdate,
   accname,
   sum(currentvalue) accountnotional
from
   agni_etl_stage_ff1
group by
   asofdate,
   accname
),
ctetickernotional as (
select
   asofdate,
   accname,
   symbol,
   currentvalue tickernotional
from
   agni_etl_stage_ff1
),  
cteallocations as ( 
select
   r.account, 
   r.symbol, 
   r.category, 
   r.allocation tickerallocation, 
   m.allocation sleeveallocation 
from
   agni_ref_category_symbol r join agni_portfolio_model m on 
      r.account = m.account and 
      r.category = m.category 
) 
select
   n.asofdate, 
   a.account accname, 
   a.category, 
   a.symbol, 
   a.tickerallocation * 100 ratio, 
   a.tickerallocation * (a.sleeveallocation * .01) * 100000 model, 
   t.tickernotional actual, 
   a.tickerallocation * (a.sleeveallocation * .01) * n.accountnotional forecast, 
   a.tickerallocation * (a.sleeveallocation * .01) * n.accountnotional -  t.tickernotional spread    
from 
   cteallocations a 
   join ctetotnotional n on 
      a.account = n.accname 
   join ctetickernotional t on 
      t.accname = n.accname and 
      t.symbol = a.symbol and 
      t.asofdate = n.asofdate    
where
   t.asofdate = :d and
   t.accname = :acc and 
   a.category = :cat
   
