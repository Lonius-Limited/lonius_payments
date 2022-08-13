frappe.ready(function () {
    // frappe.msgprint(frappe.session.user)
    $('#top')[0].scrollIntoView();
    const isAdminOrGuest = ["Guest", "Administrator"].filter(user => user == frappe.session.user)
    isAdminOrGuest.length < 1 && $('#userid').val(frappe.session.user)


    $('#customer_statement').on("click", function () {
        const USER = $('#userid').val()
        frappe.msgprint(`Getting billing for ${USER}`)
        USER.length < 1 && frappe.throw("Email or customerID not provided" + USER)
        getCustomerSubscription(USER) 
    })
    const getCustomerSubscription = (user) => {
        let response = {}
        frappe.call({
            method: "lonius_payments.customer_account_request",
            args: {
                user
            },
            freeze: true,
            freeze_message: "Please wait as we process your query",
            async: false
        }).then(res => {
            console.log(res)
            const customerStatement = res.message
            const keys = Object.keys(customerStatement)
            console.log(keys)
            const isError = keys.filter(key => key === "error").length > 0;

            if (isError) {
                // document.getElementById("divFirst").scrollIntoView();
                $('#top')[0].scrollIntoView();
                $('#userid').val("")
                $('#userid').focus()
                frappe.throw(customerStatement.error)
            }
            // isError && frappe.throw(customerStatement.error)

            let amt = format_currency(customerStatement.balance, "KES")
          


            const invoices = customerStatement.invoice_items;

            // const columns = getDataColumns()//['Reference', 'Item', 'Amount']

            // // const data = invoices.map(
            // //     row => {
            // //         let rowData = []
            // //         rowData.push(row.invoice)
            // //         rowData.push(row.item)
            // //         let rowAmt = format_currency(row.amount, "KES")
            // //         rowData.push(rowAmt)
            // //         return rowData
            // //     }
            // // )
            // // const options = { columns, data }
            // // new DataTable('#invoice_items', options)

            let invoicesHTML = invoices.map((row, idx) => {
                return `${idx+1}.<div class="col-sm-12">
                <div class="card">
                  <div class="card-body">
                    <p class="card-title">Ref: ${row.invoice} : ${row.item} </p>
                    <hr>
                    <p class="card-text">Amount: <span style="color:green">${format_currency(row.amount, "KES")} </span> </p>
                  </div>
                </div>
              </div>`
            })
            const invoicesHTMLWrapper =`<div class="row">${invoicesHTML.join("")}</div>`
            const billingSummary =`<h4>Company: ${customerStatement.customer}</h4><h5>Account Balance: ${format_currency(customerStatement.balance, "KES")}</h5><small>Deadline: ${customerStatement.grace_period_date}</small><br><br><button class="btn btn-sm btn-success">Pay Now</button>`
            // frappe.msgprint($('#statement-section').html())
            frappe.msgprint({
                title: __('Account Summary'),
                indicator: 'green',
                message: `${billingSummary} <hr> ${invoicesHTMLWrapper}`
                // message: $('#statement-section').html()
            });
            // $("#data-modal").modal({

            // })

        })
        return response
    }
})