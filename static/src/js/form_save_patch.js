/** @odoo-module **/
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("o_form_button_save")) {
            const breadcrumbLink = document.querySelector(".o_back_button a");
            const breadcrumbText = breadcrumbLink ? breadcrumbLink.textContent.trim() : "";

            // Only proceed with custom validation if we are in "Internal Transfers"
            if (breadcrumbText === "Internal Transfers") {
                // Get quantity from td.o_list_number span[data-tooltip='Quantity']
                const quantitySpan = document.querySelector("td.o_list_number span[data-tooltip='Quantity']");
                const quantity = quantitySpan ? parseFloat(quantitySpan.textContent.trim()) : 0;

                // Get product_uom_qty from div[name='product_uom_qty'] span
                const productUomQtySpan = document.querySelector("div[name='product_uom_qty'] span");
                const productUomQty = productUomQtySpan ? parseFloat(productUomQtySpan.textContent.trim()) : 0;

                console.log("Breadcrumb Text:", breadcrumbText);
                console.log("Quantity:", quantity);
                console.log("Product UOM Qty:", productUomQty);


                if (productUomQty < quantity) {
                    const userConfirmed = confirm(`Warning! Demand is (${productUomQty}) but you need quantity (${quantity}). Do you want to continue saving?`);
                    if (!userConfirmed) {
                        event.preventDefault();
                        event.stopPropagation();
                        return false;  // block save
                    }
                    // if userConfirmed is true, DO NOTHING: default save proceeds
                }
            }

            // Otherwise, proceed with normal save
        }
    }, true);

});
