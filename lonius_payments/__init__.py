
__version__ = '0.0.1'

import frappe
import requests, json


BASE_URL = "https://lonius.co.ke"
API_KEY,API_SECRET ='675432cf7ad7c2f','ab07756950a8a1c'
message_template ="""
<div class="ql-editor read-mode">
    <p><strong>Your {} Licence is expired.</strong></p>
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
    def _get_html(invoices:list):
        """
        <table class="table table-bordered" style="">
    <tbody>
        <tr>
            <td data-row="insert-column-right"><strong style="background-color: rgb(249, 250, 250);">Invoice
                    Number</strong></td>
            <td data-row="insert-column-right">Description</td>
            <td data-row="insert-column-right">Amount(KES)</td>
        </tr>
        <tr>
            <td data-row="row-zv8t">ACC-SINV-2022-00015</td>
            <td data-row="row-zv8t">Setup Fee</td>
            <td data-row="row-zv8t">5,000</td>
        </tr>
        
    </tbody>
</table>
        """
    user = frappe.session.user
    site_url = frappe.utils.get_url()
    if user == "Administrator": return
    subscription_is_valid, subscription_details = get_subscription_details(site_url, user) #Returns a Boolean
    if subscription_is_valid: return
    message = message_template.format(
        site_url,
        subscription_details.customer,
        subscription_details.invoice_due_date,
        _get_html(subscription_details.invoices),
        subscription_details.payment_settlement_details,
    )
    clear_user_roles(user=user)
    frappe.throw("<h4> {} </h4> {}".format(frappe.session.user,), title="Subscription Expired", wide=True)
def clear_user_roles(user = None):
    user = user or frappe.session.user
    if user:
        doc = frappe.get_doc("User", user)
        doc.flags.ignore_permissions = 1
        current_roles  = doc.get("roles")
        dump_roles(user, current_roles)
        doc.roles = []
        doc.save()
def dump_roles(user, roles):
    if not roles: return
    previous_dumps = frappe.get_all("User Role Dump", filters=dict(user=user))
    if  previous_dumps:
        role_list = [x.get("name") for x in previous_dumps]
        role_list.append('Some Weird Role')#Fingers crossed this is not an actual role
        docnames = tuple(role_list)
        frappe.db.sql("DELETE FROM `tabUser Role Dump` WHERE user in {}".format(docnames))
    role_to_dump = [x.get("role") for x in roles]
    
    args = dict(doctype="User Role Dump",user=user,roles=[dict(role=x) for x in role_to_dump])
    doc = frappe.get_doc(args)
    doc.flags.ignore_permissions=1
    doc.insert()

def get_subscription_details(site_url, user):
    path ="/api/method/lonius_payments.api.subscription.get_subscription_details"
    headers = dict(Authorization='token {}:{}'.format(API_KEY,API_SECRET))
    payload = dict(site_url=site_url,user=user)
    r = requests.get('{}{}'.format(BASE_URL,path), headers=headers, json=payload)
def test_connection(): 
    path = "/api/method/frappe.auth.get_logged_user"
    headers = dict(Authorization='token {}:{}'.format(API_KEY,API_SECRET))
    r = requests.get('{}{}'.format(BASE_URL,path), headers=headers)
    print(r.json())
def ttest_local_conn():
    pass
    
    