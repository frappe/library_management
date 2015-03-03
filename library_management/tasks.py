# Copyright (c) 2013, Frappe
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import date_diff, nowdate, formatdate, add_days

def daily():
	loan_period = frappe.db.get_value("Library Management Settings", None, "loan_period")

	overdue = get_overdue(loan_period)

	for member, items in overdue.iteritems():
		content = """<h2>Following Items are Overdue</h2>
		<p>Please return them as soon as possible</p><ol>"""

		for i in items:
			content += "<li>{0} ({1}) due on {2}</li>".format(i.article_name, i.article,
				formatdate(add_days(i.transaction_date, loan_period)))

		content += "</ol>"

		frappe.send(recipients=[frappe.db.get_value("Library Member", member, "email_id")],
			sender="test@example.com", subject="Library Articles Overdue", msg=content, bulk=True)

def get_overdue(loan_period):
	# check for overdue articles
	today = nowdate()

	overdue_by_member = {}
	articles_transacted = []

	for d in frappe.db.sql("""select name, article, article_name, library_member, member_name
		from `tabLibrary Transaction` order by transaction_date desc, modified desc""", as_dict=1):

		if d.article in articles_transacted:
			continue

		if d.transaction_type=="Issue" and date_diff(today, d.transaction_date) > loan_period:
			overdue_by_member.setdefault(d.library_member, [])
			overdue_by_member[d.library_member].append(d)

		articles_transacted.append(d.article)
