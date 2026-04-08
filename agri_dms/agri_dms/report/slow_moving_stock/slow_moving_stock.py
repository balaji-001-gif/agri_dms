import frappe
def execute(filters=None):
	columns = [{'label':'Distributor','fieldname':'distributor','width':160}, {'label':'Machine','fieldname':'machine_name','width':150}, {'label':'Days in Stock','fieldname':'days','fieldtype':'Int'}]
	# Dummy logic for example
	data = []
	return columns, data
