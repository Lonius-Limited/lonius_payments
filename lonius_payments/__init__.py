__version__ = "0.0.1"

import frappe
import requests, json


BASE_URL = "https://lonius.co.ke"
API_KEY, API_SECRET = "675432cf7ad7c2f", "ab07756950a8a1c"
message_template = """
<div class="ql-editor read-mode">
    <p><strong>Your usage Licence is expired.</strong></p>
    <p><br></p>
    <blockquote>Please remit your subscription fee arrears in the account details below to avoid account suspension and
        data loss.</blockquote>
    <p><br></p>
    <p><strong style="color: rgb(161, 0, 0);">INVOICE TO: &nbsp;{}</strong></p>
    <p><strong style="color: rgb(161, 0, 0);"><u>INVOICE DUE: {}</u></strong></p>
    {}
    <p><br></p>
    {}
</div>
"""
def check_subscription():
    user = frappe.session.user
    # site_url = frappe.utils.get_url()
    if user == "Administrator":
        return
    company = get_default_user_company(user) or "-"
    res = get_subscription_details(company)
    frappe.msgprint(f"{res}")

    # clear_user_roles(user=user)
    # frappe.throw(
    #     "<h4> {} </h4> {}".format(frappe.session.user, "-"),
    #     title="Subscription Expired",
    #     wide=True,
    # )


def clear_user_roles(user=None):
    user = user or frappe.session.user
    if user:
        doc = frappe.get_doc("User", user)
        doc.flags.ignore_permissions = 1
        current_roles = doc.get("roles")
        dump_roles(user, current_roles)
        doc.roles = []
        doc.save()


def dump_roles(user, roles):
    if not roles:
        return
    previous_dumps = frappe.get_all("User Role Dump", filters=dict(user=user))
    if previous_dumps:
        role_list = [x.get("name") for x in previous_dumps]
        role_list.append(
            "Some Weird Role"
        )  # Fingers crossed this is not an actual role
        docnames = tuple(role_list)
        frappe.db.sql(
            "DELETE FROM `tabUser Role Dump` WHERE user in {}".format(docnames)
        )
    role_to_dump = [x.get("role") for x in roles]

    args = dict(
        doctype="User Role Dump", user=user, roles=[dict(role=x) for x in role_to_dump]
    )
    doc = frappe.get_doc(args)
    doc.flags.ignore_permissions = 1
    doc.insert()

@frappe.whitelist()
def get_subscription_details(customer):
    # path = "/api/method/lonius_payments.api.subscription.get_customer_subscription"
    #get_subscription_details
    path = "/api/method/lonius_payments.api.subscription.get_subscription_details"
    headers = dict(Authorization="token {}:{}".format(API_KEY, API_SECRET))
    # payload = dict(customer=customer)
    payload = dict(user="dsmwaura@gmail.com",site_url="ploti.cloud")
    r = requests.get("{}{}".format(BASE_URL, path), headers=headers, json=payload)
    return r.json()


def test_connection():
    path = "/api/method/lonius_payments.api.subscription."
    headers = dict(Authorization="token {}:{}".format(API_KEY, API_SECRET))
    r = requests.get("{}{}".format(BASE_URL, path), headers=headers)
    print(r.json())


def ttest_local_conn():
    pass
def get_default_user_company(user):
    args = dict(allow="Company", user=user)
    return frappe.get_value("User Permission",args,"for_value")