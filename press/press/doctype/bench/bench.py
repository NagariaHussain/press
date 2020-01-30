# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document
import json
import requests
from frappe.utils.password import get_decrypted_password


class Bench(Document):
	def validate(self):
		if not self.candidate:
			candidate = frappe.get_all("Deploy Candidate", filters={"group": self.group})[0]
			self.candidate = candidate.name
		candidate = frappe.get_doc("Deploy Candidate", self.candidate)
		if not self.apps:
			for release in candidate.apps:
				scrubbed = frappe.get_value("Frappe App", release.app, "scrubbed")
				self.append(
					"apps", {"app": release.app, "scrubbed": scrubbed, "hash": release.hash}
				)

	def after_insert(self):
		self.create_agent_request()

	def create_agent_request(self):
		agent = Agent(self.server)
		agent.new_bench(self)


class Agent:
	def __init__(self, server, server_type="Server"):
		self.server_type = server_type
		self.server = server
		self.port = 80

	def new_bench(self, bench):
		config = {
			"background_workers": 4,
			"frappe_user": "frappe",
			"mail_login": "test@example.com",
			"mail_password": "test",
			"mail_server": "smtp.example.com",
			"monitor": True,
			"redis_cache": "redis://localhost:13000",
			"redis_queue": "redis://localhost:11000",
			"redis_socketio": "redis://localhost:12000",
			"server_script_enabled": True,
			"socketio_port": 9000,
			"webserver_port": 8000,
			"admin_password": "admin",
			"root_password": "root",
			"developer_mode": True,
		}

		data = {
			"config": config,
			"apps": [],
			"name": bench.name,
			"python": "/usr/bin/python3.6",
		}
		for app in bench.apps:
			repo, branch = frappe.db.get_value("Frappe App", app.app, ["url", "branch"])
			data["apps"].append(
				{"name": app.scrubbed, "repo": repo, "branch": branch, "hash": app.hash}
			)

		job = self.create_agent_job("New Bench", "benches", data, bench=bench.name)
		job_id = self.post("benches", data)["job"]
		job.job_id = job_id
		job.save()

	def new_site(self, site):
		apps = [frappe.db.get_value("Frappe App", app.app, "scrubbed") for app in site.apps]
		data = {
			"config": {"monitor": True, "developer_mode": True},
			"apps": apps,
			"name": site.name,
			"mariadb_root_password": get_decrypted_password(
				"Server", site.server, "mariadb_root_password"
			),
			"admin_password": get_decrypted_password("Site", site.name, "admin_password"),
		}

		job = self.create_agent_job(
			"New Site", f"benches/{site.bench}/sites", data, bench=site.bench, site=site.name
		)
		job_id = self.post(f"benches/{site.bench}/sites", data)["job"]
		job.job_id = job_id
		job.save()

	def new_domain(self, domain):
		data = {"name": domain}
		job = self.create_agent_job("Add Host to Proxy", "proxy/hosts", data)
		job_id = self.post(f"proxy/hosts", data)["job"]
		job.job_id = job_id
		job.save()

	def new_server(self, server):
		data = {"name": server}
		job = self.create_agent_job(
			"Add Upstream to Proxy", "proxy/upstreams", data, upstream=server
		)
		job_id = self.post(f"proxy/upstreams", data)["job"]
		job.job_id = job_id
		job.save()

	def new_upstream_site(self, server, site):
		data = {"name": site}
		job = self.create_agent_job(
			"Add Site to Upstream",
			f"proxy/upstreams/{server}/sites",
			data,
			site=site,
			upstream=server,
		)
		job_id = self.post(f"proxy/upstreams/{server}/sites", data)["job"]
		job.job_id = job_id
		job.save()

	def ping(self):
		return self.get(f"ping")["message"]

	def post(self, path, data):
		url = f"http://{self.server}:{self.port}/agent/{path}"
		password = get_decrypted_password(self.server_type, self.server, "agent_password")
		headers = {"Authorization": f"bearer {password}"}
		result = requests.post(url, headers=headers, json=data)
		try:
			return result.json()
		except:
			frappe.log_error(result.text, title="Agent Request Exception")

	def get(self, path):
		url = f"http://{self.server}:{self.port}/agent/{path}"
		password = get_decrypted_password(self.server_type, self.server, "agent_password")
		headers = {"Authorization": f"bearer {password}"}
		result = requests.get(url, headers=headers)
		try:
			return result.json()
		except:
			frappe.log_error(result.text, title="Agent Request Exception")

	def create_agent_job(self, job_type, path, data, bench=None, site=None, upstream=None):
		job = frappe.get_doc(
			{
				"doctype": "Agent Job",
				"server_type": self.server_type,
				"server": self.server,
				"bench": bench,
				"site": site,
				"upstream": upstream,
				"status": "Pending",
				"request_method": "POST",
				"request_path": path,
				"request_data": json.dumps(data, indent=4, sort_keys=True),
				"job_type": job_type,
			}
		).insert()
		return job

	def get_job_status(self, id):
		status = self.get(f"jobs/{id}")
		return status

	def update(self):
		return self.post("update", {})
