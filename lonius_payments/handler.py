import frappe
import erpnext
import requests
import json
# short_code = "603021"
short_code = "3033421"
prod_consumer_key = "I7j4D3tNG95utx5mDjVk9O0BKxDuofV6"
prod_consumer_secret = "UW4i7rSl4eiuF8LN"
# api_host = "https://sandbox.safaricom.co.ke"
api_host = "https://api.safaricom.co.ke"
#bench new-site salim.bizpok.com --admin-password 'velo@2020' --mariadb-root-username erpuser --mariadb-root-password 'velo@2020'

#git remote add salimrepo https://dsmwaura:saleem-2013@gitlab.com/dsmwaura/facility_management.git

#https://dsmwaura:saleem2013-@@gitlab.com/dsmwaura/personal_portfolio.git
# mpesa event handlers

def get_access_token():

    consumer_key = prod_consumer_key
    consumer_secret = prod_consumer_secret
    api_URL = '{}/oauth/v1/generate?grant_type=client_credentials'.format(api_host)
    r = requests.get(api_URL, auth=requests.auth.HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = json.loads(r.text)

    return access_token['access_token']

@frappe.whitelist(allow_guest=True)
def register_urls():

    access_token = get_access_token()
    
    api_url = "{}/mpesa/c2b/v1/registerurl".format(api_host)
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode": short_code,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://lonius.co.ke/api/method/lonius_payments.handler.confirm",
        "ValidationURL": "https://lonius.co.ke/api/method/lonius_payments.handler.validate"
    }
    response = requests.post(api_url, json=options, headers=headers)
    response = json.loads(response.text)

    frappe.local.response.update(response)

@frappe.whitelist(allow_guest=True)
def confirm(*args, **kwargs):

    data = kwargs
    frappe.logger("frappe.web").debug(kwargs)
    amount = kwargs['TransAmount']
    account_number = data['BillRefNumber']
    tx_reference = data['TransID']
    phone_number = data['MSISDN']


    try:
        payment = frappe.get_doc({
            "doctype":"MPESA Payments",
            "phone_number":phone_number,
            "reference_number":tx_reference,
            "bill_reference_number": account_number,
            "raw_json_response":json.dumps(data),
            "amount": amount,
            "transaction_time":data['TransTime'],
            "sender_name":  "{} {} {}".format(data['FirstName'], data['MiddleName'], data['LastName']) 
        })
        payment.run_method('set_missing_values')
        payment.insert(
            ignore_permissions=True,
            ignore_links=True,
        )
        payment.submit()
        frappe.db.commit()
        payment.notify_update()
        
        frappe.logger("frappe.web").debug(payment)

    except Exception as e:
        frappe.logger("frappe.web").debug({"error":str(e)})

    frappe.local.response.update({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        })
    return

@frappe.whitelist(allow_guest=True)
def validate(*args, **kwargs):
    frappe.logger("frappe.web").debug(kwargs)

    try:
        if (1 > 0):
            frappe.local.response.update({
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            })

    except Exception as e:
        frappe.local.response.update({
            "ResultCode":1, 
            "ResultDesc":"Failed"
        })
    
    return


@frappe.whitelist(allow_guest=True)
def simulate_tx(*args, **kwargs):

    access_token = get_access_token()
    api_url = "{}/mpesa/c2b/v1/simulate".format(api_host)
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "ShortCode": short_code,
        "CommandID": "CustomerBuyGoodsOnline",
        "Amount": kwargs['amount'],
        "Msisdn": "254708374149",
        "BillRefNumber": kwargs['account_no']
    }
    response = requests.post(api_url, json=request, headers=headers)
    response = json.loads(response.text)

    frappe.local.response.update(response)
def test_existence():
    print("I exist....")

#bench new-site dev.lonius.com --admin-password 'velo@2020' --mariadb-root-username erpnext --mariadb-root-password 'velo@2020'