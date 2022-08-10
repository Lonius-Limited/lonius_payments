from . import __version__ as app_version

app_name = "lonius_payments"
app_title = "Lonius Payments"
app_publisher = "Lonius Devs"
app_description = "App for managing client payments"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@lonius.co.ke"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lonius_payments/css/lonius_payments.css"
app_include_js = "/assets/lonius_payments/js/frappe/lonius_payments.js"

# include js, css files in header of web template
# web_include_css = "/assets/lonius_payments/css/lonius_payments.css"
# web_include_js = "/assets/lonius_payments/js/lonius_payments.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lonius_payments/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "lonius_payments.install.before_install"
# after_install = "lonius_payments.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lonius_payments.uninstall.before_uninstall"
# after_uninstall = "lonius_payments.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lonius_payments.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lonius_payments.tasks.all"
# 	],
# 	"daily": [
# 		"lonius_payments.tasks.daily"
# 	],
# 	"hourly": [
# 		"lonius_payments.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lonius_payments.tasks.weekly"
# 	]
# 	"monthly": [
# 		"lonius_payments.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "lonius_payments.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lonius_payments.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lonius_payments.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------
on_session_creation = "lonius_payments.check_subscription"

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lonius_payments.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
