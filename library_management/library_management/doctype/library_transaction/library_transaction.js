cur_frm.add_fetch("article", "article_name", "article_name");

frappe.ui.form.on("Library Transaction", "library_member", function(frm) {
	$.ajax({
		url:"/api/resource/Library Member/" + frm.doc.library_member,
		statusCode: {
			200: function(data) {
				frappe.model.set_value(frm.doctype, frm.docname, "member_name",
					data.data.first_name
					+ (data.data.last_name ? (" " + data.data.last_name) : ""))
			}
		}
	})
})
