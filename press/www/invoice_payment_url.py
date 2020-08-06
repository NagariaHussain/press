# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from press.api.account import redirect_to


def get_context(context):
	invoice = frappe.get_doc("Invoice", frappe.form_dict.name)
	redirect_to(invoice.stripe_invoice_url)
