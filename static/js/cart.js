
$(document).ready(function () {
    $(".decrease-quantity, .increase-quantity, .delete").on("click", function () {
        var sizeId = $(this).data("item-id");
        var maxQuantity = $(this).data("max-quantity");
        var action = $(this).data("action");
        var word = "quantity" + sizeId;  // Construct the ID dynamically
        var quantityElement = document.getElementById(word); // Use the dynamically constructed ID
        var currentQuantity = parseInt(quantityElement.innerText, 10);

        if (action === "decrease" && currentQuantity > 0) {
            currentQuantity -= 1;
            console.log(sizeId, currentQuantity);
        } else if (action === "increase" && currentQuantity < maxQuantity) {
            currentQuantity += 1;
            console.log(sizeId, currentQuantity);
        } else if (action === "delete" && currentQuantity > 0) {
            currentQuantity = 0;
            console.log(sizeId, currentQuantity);
        }


        // Update the quantity display
        quantityElement.innerText = currentQuantity;

        // Make an AJAX request to update the session cart
        $.ajax({
            url: "/update-cart/",
            type: "GET",
            data: {
                size: sizeId,
                new_quantity: currentQuantity
            },
            success: function (data) {

                location.reload();



                // Update successful, you can handle any additional UI updates here

            },
            error: function () {
                // Handle errors, if any
            }
        });
    });
});

