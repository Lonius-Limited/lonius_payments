__version__ = "0.0.1"

import frappe
import requests, json
from frappe.sessions import Session, clear_sessions, delete_session
from datetime import datetime, date
from frappe.utils.data import fmt_money, add_days


BASE_URL = "https://lonius.co.ke"
API_KEY, API_SECRET = "675432cf7ad7c2f", "ab07756950a8a1c"
MESSAGE_TEMPLATE = """
<div class="container">
    <p><strong>Your account is temporarily locked which means you cannot access your portal to create or approve transactions. This action is supported by {}.</strong></p>
    
    
    <p><strong style="color: rgb(161, 0, 0);">Your Company: &nbsp;<u>{}</u></strong></p>

    <blockquote>If you believe that this message in error, please contact your ERP Implementer on <em style="color:green">info@lonius.co.ke</em> on or before <u>{}</u>, for restoration of your account.</blockquote>
    
</div>
"""
def check_subscription():
    user = frappe.session.user
    # site_url = frappe.utils.get_url()
    if user == "Administrator":
        return
    company = get_default_user_company(user) or "-"
    res = get_subscription_details(company)

    if "error" in list(res.keys()):
        clear_sessions(user, keep_current=False)
        frappe.throw('{}'.format(res.get("error")), title="Your account is locked")
        return
    balance, last_payment_date = res.get("balance"), res.get("latest_payment_date")
    latest_payment_date = datetime.strptime(last_payment_date,"%Y-%m-%d")
    deadline = add_days(latest_payment_date, 40).date()
    if float(balance) > 0.0 and deadline < date.today():#30 days and 10 days grace
    # if float(balance) > 0.0:
        clear_sessions(user, keep_current=False)
        msg = MESSAGE_TEMPLATE.format(
            "<a target=_blank href='{}/toc'>Lonius ERP Terms and Conditions</a>".format(BASE_URL),
            res.get("customer"),
            deadline.strftime("%B, %d %Y"),
        )
        frappe.throw(msg, title="Lonius Usage Alert", wide=True)     
@frappe.whitelist()
def get_subscription_details(customer):
    path = "/api/method/lonius_payments.api.subscription.get_customer_subscription"
    headers = dict(Authorization="token {}:{}".format(API_KEY, API_SECRET))
    payload = dict(customer=customer)
    r = requests.get("{}{}".format(BASE_URL, path), headers=headers, json=payload)
    return (r.json()).get("message")
def test_connection():
    path = "/api/method/lonius_payments.api.subscription."
    headers = dict(Authorization="token {}:{}".format(API_KEY, API_SECRET))
    r = requests.get("{}{}".format(BASE_URL, path), headers=headers)
    print(r.json())
@frappe.whitelist(allow_guest=True)
def customer_account_request(user):
    company = get_default_user_company(user) or '-'
    res = get_subscription_details(company)
    return res
def get_default_user_company(user):
    args = dict(allow="Company", user=user)
    return frappe.get_value("User Permission",args,"for_value")

def alert_logged_in_users():
    frappe.publish_realtime(event="subscription_expired",message=dict(expired="Yes") ,doctype="BOM",docname="", user=frappe.session.user)
    # frappe.publish_realtime(event='eval_js', message='alert("{0}")'.format("msg_var"), user="anotheradmin@lonius.co.ke")
    print("Alerted")