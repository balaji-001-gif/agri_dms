import frappe
def execute(filters=None):
	columns = [
		{'label':'Distributor','fieldname':'distributor','fieldtype':'Link','options':'Distributor','width':160},
		{'label':'Region','fieldname':'region','fieldtype':'Data','width':100},
		{'label':'Orders','fieldname':'total_orders','fieldtype':'Int','width':70},
		{'label':'Revenue','fieldname':'total_revenue','fieldtype':'Currency','width':120}
	]
	data = frappe.db.sql('''
		SELECT cs.distributor, d.region, COUNT(cs.name) as total_orders, SUM(cs.total_amount) as total_revenue
		FROM `tabCustomer Sale` cs
		JOIN `tabDistributor` d ON cs.distributor = d.name
		WHERE cs.status = 'Confirmed'
		GROUP BY cs.distributor
	''', as_dict=True)
	return columns, data
