with ctetotnotional as (
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
ctesleevenotional as ( 
select
   f.asofdate, 
   f.accname, 
   m.category, 
   round(sum(f.currentvalue), 0) sleevenotional
from 
   agni_ref_category_symbol m join agni_etl_stage_ff1 f on 
      f.accname = m.account and 
      f.symbol = m.symbol
group by 
   f.asofdate, 
   f.accname,     
   m.category 
), 
cteactual as ( 
select
   t.asofdate, 
   t.accname, 
   s.category, 
   round(s.sleevenotional/t.accountnotional * 100, 2) actualpercent,
   s.sleevenotional actual 
from
   ctetotnotional t join ctesleevenotional s on 
      t.asofdate = s.asofdate and 
      t.accname = s.accname 
),
cteexpected as (
select
   n.asofdate, 
   m.account, 
   m.category, 
   m.id categoryid, 
   m.allocation, 
   round(m.allocation * n.accountnotional * 0.01) expected
from 
   agni_portfolio_model m join ctetotnotional n on 
      n.accname = m.account 
)
select
   a.asofdate, 
   a.accname, 
   e.category, 
   e.allocation,
   e.allocation * 1000 actualpercent,
   -- a.actualpercent,
   a.actual,  
   e.expected, 
   e.expected - a.actual difference      
from 
   cteactual a join cteexpected e on 
      a.asofdate = e.asofdate and 
      a.accname = e.account and 
      a.category = e.category
where
   a.asofdate = :d and 
   a.accname = :acc
order by 
   e.categoryid

-- 2018-11-08   X70974968   127777.4200   

