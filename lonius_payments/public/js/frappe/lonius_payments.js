frappe.ui.form.on('BOM', {
    setup(frm){
        frappe.realtime.on("subscription_expired", function(msg) {
            console.log("Logging this coz I can")
            var dialog = frappe.msgprint({
                message:__("The Version you are using expired already man"),
                indicator: 'green',
                title: __('Subscription Expired')
            });
            dialog.set_primary_action(__("Okay"), function() {
                location.reload(true);
            });
            dialog.get_close_btn().toggle(false);
        });
    },
    refresh(frm){
        console.log("Logging this at refresh")
    }
})
