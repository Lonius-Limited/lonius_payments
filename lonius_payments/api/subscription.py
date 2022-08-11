from decimal import InvalidContext
from urllib.parse import uses_relative
import frappe

from erpnext.selling.doctype.customer.customer import get_customer_outstanding
from frappe.utils.data import fmt_money, add_days

DEFAULT_COMPANY = frappe.defaults.get_defaults()["company"]
from datetime import datetime, date


@frappe.whitelist()
def get_subscription_details(user=None, site_url=None):
    if not (user and site_url):
        return dict(
            error="User ID or originating client traffic unrecognized or is not provided in the request body"
        )
    lonius_client = frappe.get_value(
        "Lonius Client",
        dict(userid=user, site_url=site_url, docstatus=1),
        ["customer", "last_payment", "last_payment_date"],
        as_dict=1,
    )
    if not lonius_client:
        return dict(error="Client file missing")
    customer = lonius_client.get("customer")
    return get_customer_subscription(customer=customer)


@frappe.whitelist()
def get_customer_subscription(customer=None, user=None, site_url=None):
    if customer == "" or customer is None:
        # if not lonius_client:
        return dict(error="Client ID was not provided")
    if not frappe.get_value("Customer", customer, "name"):
        return dict(
            error="Client ID provided ({}) did not match any records in our database".format(
                customer
            )
        )
    invoices = [
        dict(id=x.get("name"), due_date=x.get("due_date"))
        for x in frappe.get_all(
            "Sales Invoice",
            filters=dict(
                customer=customer, status=["IN", ["Partly Paid", "Unpaid", "Overdue"]]
            ),
            fields=["*"],
        )
    ]

    pending_invoices = [x.get("id") for x in invoices]
    items = [
        dict(item=x.get("description"), amount=x.get("amount"), invoice=x.get("parent"))
        for x in frappe.get_all(
            "Sales Invoice Item",
            filters=dict(parent=["IN", pending_invoices]),
            fields=["*"],
        )
    ]
    balance = get_customer_outstanding(customer, DEFAULT_COMPANY, True)

    recent_payment = [
        x.get("posting_date")
        for x in frappe.get_all(
            "Payment Entry",
            filters=dict(party=customer, payment_type="Receive"),
            fields=["posting_date"],
            order_by="creation desc",
            page_length=1,
        )
    ]
    latest_payment_date = date.today().replace(day=1)

    if len(recent_payment) > 0:
        if recent_payment[0]:
            latest_payment_date = recent_payment[0]

    collection_account = frappe.get_value(
        "Terms and Conditions", "Lonius Limited Account Details", "terms"
    )  # HardCoded

    latest_payment_exceeded_grace_period = (
        add_days(latest_payment_date, 44) < date.today()
    )

    customer_details = dict(
        site_url=site_url,
        user=user,
        customer=customer,
        invoices=invoices,
        invoice_items=items,
        balance=balance,
        latest_payment_date=latest_payment_date,
        grace_period_date=add_days(latest_payment_date, 40),
        collection_account=collection_account,
        exceeded_grace_period=latest_payment_exceeded_grace_period,
    )
    if not user:
        customer_details.pop("user")
    if not site_url:
        customer_details.pop("site_url")
    return customer_details or dict(error="No client details returned")


@frappe.whitelist()
def sample_subscription_details():
    # user, url = "racheal@nakuru.com", "paperless.nakuru.com"
    customer = "ValueFarm Feeds Limited"
    return get_customer_subscription(customer=customer)
