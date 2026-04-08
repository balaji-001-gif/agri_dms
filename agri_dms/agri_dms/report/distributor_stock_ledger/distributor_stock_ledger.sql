SELECT 
	ds.distributor, m.machine_name, ds.qty_in_hand, ds.location
FROM `tabDistributor Stock` ds
JOIN `tabMachine` m ON ds.machine = m.name
WHERE ds.qty_in_hand > 0
