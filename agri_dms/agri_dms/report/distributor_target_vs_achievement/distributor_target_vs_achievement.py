import frappe
def execute(filters=None):
	columns = [
		{'label':'Distributor','fieldname':'distributor','fieldtype':'Link','options':'Distributor','width':160},
		{'label':'Target','fieldname':'target_amount','fieldtype':'Currency','width':120},
		{'label':'Achieved','fieldname':'achieved_amount','fieldtype':'Currency','width':120},
		{'label':'Achievement %','fieldname':'achievement_pct','fieldtype':'Float','width':100}
	]
	data = frappe.db.sql('''
		SELECT dt.distributor, dt.target_amount, COALESCE(SUM(cs.total_amount), 0) as achieved_amount
		FROM `tabDistributor Target` dt
		LEFT JOIN `tabCustomer Sale` cs ON cs.distributor = dt.distributor AND cs.status = 'Confirmed'
		GROUP BY dt.distributor
	''', as_dict=True)
	for d in data:
		d['achievement_pct'] = (d['achieved_amount'] / d['target_amount'] * 100) if d['target_amount'] else 0
	return columns, data
