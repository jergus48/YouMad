$(document).ready(function () {
  var quantityElement = $("#quantity");
  var increaseButton = $("#increase");
  var decreaseButton = $("#decrease");
  updateMaxQuantity();
  // Listen for changes in the size select
  $("#size").on("change", function () {
    updateMaxQuantity();
  });

  decreaseButton.on("click", function () {
    var currentQuantity = parseInt(quantityElement.text());
    if (currentQuantity > 1) {
      currentQuantity -= 1;
      quantityElement.text(currentQuantity);
    }
  });

  // Increase quantity button
  increaseButton.on("click", function () {
    var currentQuantity = parseInt(quantityElement.text());
    var maxQuantity = increaseButton.attr("data-max-quantity");
    if (currentQuantity < maxQuantity) {
      currentQuantity += 1;
      quantityElement.text(currentQuantity);
    }
  });

  function updateMaxQuantity() {
    var selectedSize = $("#size option:selected");
    var productId = selectedSize.data("product");
    var size = selectedSize.data("size");

    // Make an AJAX request to fetch the quantity from the server
    $.ajax({
      url: "/get-size-quantity/",
      type: "GET",
      data: {
        product_id: productId,
        size: size
      },
      success: function (data) {
        // Update the max attribute of the quantity input
        var maxQuantity = data.quantity;
        increaseButton.attr("data-max-quantity", maxQuantity);

        // Update the min attribute based on the quantity
        if (maxQuantity === 0) {
          quantityElement.text(0);
        } else {
          quantityElement.text(1);
        }
      },
      error: function () {
        // Handle errors, if any
      }
    });
  }
  var addedText = document.getElementById("added")
  $("#submit").on("click", function () {
    addToCart();
    addedText.style.display = "block";
    setTimeout(function () {
      addedText.style.display = "none";
    }, 2500);

  });

  function addToCart() {
    var selectedSize = $("#size option:selected");
    var quantityElement = document.getElementById("quantity"); // Use the dynamically constructed ID
    var quantity = parseInt(quantityElement.innerText, 10);

    var size = selectedSize.data("size");

    // Make an AJAX request to fetch the quantity from the server
    $.ajax({
      url: "/addtocart/",
      type: "GET",
      data: {
        quantity: quantity,
        size: size
      },
      success: function (data) {
        // Update the max attribute of the quantity input
        console.log("added to cart")

      },
      error: function () {
        // Handle errors, if any
      }
    });
  }
});