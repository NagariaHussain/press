// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Proxy Server', {
	refresh: function(frm) {
		frm.add_custom_button(__('Ping'), () => {
			frm.call({method: "ping", doc: frm.doc, callback: result => frappe.msgprint(result.message)});
		});
		frm.add_custom_button(__('Jobs'), () => {
			const filters = {server: frm.doc.name};
			frappe.set_route("List", "Agent Job", filters);
		});
		frm.add_custom_button(__('Update Agent'), () => {
			frm.call({method: "update_agent", doc: frm.doc, callback: result => frappe.msgprint(result.message)});
		});
	}
});
