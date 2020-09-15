# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class SiteRequestLog(Document):
	pass


def send_notification_for_sites_near_quota():
	percentage = (
		frappe.db.get_single_value("Press Settings", "notify_after_quota_consumed_by") or 75
	)
	teams = frappe.get_all(
		"Team", fields=["name", "user"], filters={"enabled": True, "free_account": False}
	)
	plans = {
		plan.name: plan.cpu_time_per_day
		for plan in frappe.get_all("Plan", fields=["name", "cpu_time_per_day"])
	}
	for team in teams:
		sites_to_notify = find_sites_near_quota(team, plans, percentage)
		if sites_to_notify:
			send_team_notification_for_sites_near_quota(team.name, sites_to_notify, percentage)


def find_sites_near_quota(team, plans, percentage):
	sites = frappe.get_all(
		"Site",
		fields=["name", "plan"],
		filters={"status": "Active", "free": False, "team": team},
	)
	for site in sites:
		last_request = frappe.get_all(
			"Site Request Log",
			fields=["counter"],
			filters={"site": site.name},
			order_by="timestamp desc",
			limit=1,
		)
		sites_to_notify = []
		if last_request:
			usage = int(last_request[0].counter or 0) / (3600 * 1000 * 1000)
			plan_limit = plans[site.plan]
			if 100 * usage / plan_limit > percentage:
				sites_to_notify.append(site)
	return sites_to_notify


def send_team_notification_for_sites_near_quota(team, sites, percentage):
	for site in sites:
		site.link = frappe.utils.get_url(f"/dashboard/#/sites/{site.name}/plan")

	# TODO: Change this to team.user
	email = frappe.db.get_value("User", "Administrator", "email")
	frappe.sendmail(
		recipients=email,
		subject="Your sites are about to reach the plan limit on Frappe Cloud",
		template="sites_near_quota",
		args={
			"subject": "Your sites are about to reach the plan limit on Frappe Cloud",
			"sites": sites,
			"percentage": percentage,
		},
	)


def on_doctype_update():
	frappe.db.add_index("Site Request Log", ["site", "timestamp"])
