frappe.query_reports["Machine-wise Sales Analysis"] = {
	"filters": [
		{
			"fieldname": "manufacturer",
			"label": __("Manufacturer"),
			"fieldtype": "Link",
			"options": "Manufacturer"
		},
		{
			"fieldname": "category",
			"label": __("Category"),
			"fieldtype": "Link",
			"options": "Machine Category"
		}
	]
};
