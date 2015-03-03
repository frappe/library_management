# Copyright (c) 2013, Frappe
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Article(Document):
	def get_status(self):
		last_transaction = frappe.get_list("Library Transaction",
			fields=["transaction_type"],
			filters = {
				"article": self.name,
			}, order_by="transaction_date desc", limit_page_length=1)

		return "Taken" if (last_transaction and last_transaction[0].transaction_type == "Issue") \
			else "Available"


	def make_view(self):
		# last transaction
		self.status = self.get_status()
