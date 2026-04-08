SELECT 
	MONTHNAME(sale_date) as month, 
	YEAR(sale_date) as year, 
	COUNT(name) as orders, 
	SUM(total_amount) as revenue
FROM `tabCustomer Sale`
WHERE status = 'Confirmed'
GROUP BY YEAR(sale_date), MONTH(sale_date)
