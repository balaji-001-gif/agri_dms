import frappe
def execute(filters=None):
	columns = [
		{'label':'Machine','fieldname':'machine_name','fieldtype':'Data','width':150},
		{'label':'Qty Sold','fieldname':'qty_sold','fieldtype':'Int','width':70},
		{'label':'Revenue','fieldname':'revenue','fieldtype':'Currency','width':120}
	]
	data = frappe.db.sql('''
		SELECT m.machine_name, SUM(si.qty) as qty_sold, SUM(si.amount) as revenue
		FROM `tabSale Item` si
		JOIN `tabMachine` m ON si.machine = m.name
		JOIN `tabCustomer Sale` cs ON si.parent = cs.name
		WHERE cs.status = 'Confirmed'
		GROUP BY m.name
	''', as_dict=True)
	return columns, data
