import frappe
def execute(filters=None):
	columns = [{'label':'Distributor','fieldname':'distributor','width':160}, {'label':'Total Commission','fieldname':'total_comm','fieldtype':'Currency'}]
	data = frappe.db.sql('''
		SELECT distributor, SUM(commission_amount) as total_comm
		FROM `tabCommission Ledger`
		GROUP BY distributor
	''', as_dict=True)
	return columns, data
