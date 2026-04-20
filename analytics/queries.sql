--Top 5 agents by number of listings
select a.full_name, count(l.id) as total_listings
from agents a 
join listings l on a.id = l.agent_id
group by a.full_name
order by total_listings desc
limit 5;

--Total revenue per agent
select a.full_name, sum(t.final_price) as total_revenue
from agents a 
join transactions t on a.id = t.agent_id
group by a.full_name
order by total_revenue desc
limit 5;

--Average property price by city
select p.city ,avg(p.price) as avg_price
from properties p
group by p.city
order by avg_price desc
limit 5;

--Most common payment mode
select t.payment_mode, count(t.id) as common_mode
from transactions t
group by t.payment_mode
order by common_mode desc;

--Lead conversion rate
select p.title, count(distinct l.id) as total_leads, 
count(distinct t.id) as total_transactions
from properties p
left join leads l on p.id = l.property_id
left join listings k on p.id = k.property_id
left join transactions t on k.id = t.listing_id
group by p.title
order by total_leads desc
limit 5;
