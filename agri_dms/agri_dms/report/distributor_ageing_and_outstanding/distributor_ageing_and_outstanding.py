import frappe
from frappe.utils import date_diff, nowdate
def execute(filters=None):
	columns = [{'label':'Distributor','fieldname':'distributor','width':160}, {'label':'Outstanding','fieldname':'outstanding','fieldtype':'Currency','width':120}]
	data = frappe.db.sql('''
		SELECT distributor, SUM(total_amount) as outstanding
		FROM `tabCustomer Sale`
		WHERE status = 'Confirmed'
		GROUP BY distributor
	''', as_dict=True)
	return columns, data
