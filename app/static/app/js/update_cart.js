document.addEventListener("DOMContentLoaded", function () {
  // Attach event listeners to quantity increment/decrement buttons
  document.querySelectorAll(".qtyBtn").forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault();

      const itemId = this.dataset.id; // Get item ID from data-id
      const inputField = document.querySelector(
        `.product-form__input[data-id='${itemId}']`
      );
      const totalField = document.querySelector(`#total-${itemId}`); // Item total field
      const priceField = inputField
        .closest("tr")
        .querySelector(".cart__price-wrapper .money");
      const pricePerUnit =
        parseFloat(priceField.textContent.replace("$", "").trim()) || 0;

      let quantity = parseInt(inputField.value) || 1;

      // Adjust quantity based on button clicked
      if (this.classList.contains("plus")) {
        quantity++;
      } else if (this.classList.contains("minus")) {
        quantity = Math.max(1, quantity - 1);
      }

      inputField.value = quantity; // Update input field with new quantity

      // Calculate and update total for this item
      const totalPrice = pricePerUnit * quantity;
      totalField.textContent = `$${totalPrice.toFixed(2)}`;

      // Update subtotal for all items
      updateSubtotal();
    });
  });

  // Function to calculate and update the subtotal
  function updateSubtotal() {
    let subtotal = 0;

    // Sum up all total prices
    document.querySelectorAll(".cart-price .money").forEach((field) => {
      const price = parseFloat(field.textContent.replace("$", "").trim()) || 0;
      subtotal += price;
    });

    // Update the subtotal field
    const subtotalField = document.querySelector("#subtotal");
    if (subtotalField) {
      subtotalField.textContent = `$${subtotal.toFixed(2)}`;
    }
  }

  // Call updateSubtotal initially to ensure correct display on page load
  updateSubtotal();
});
