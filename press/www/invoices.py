# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from press.api.account import redirect_to
from frappe.utils.print_format import download_pdf


def get_context(context):
	invoice_name = frappe.form_dict.name
	default_format = frappe.get_meta("Invoice").default_print_format
	download_pdf("Invoice", invoice_name, default_format)
