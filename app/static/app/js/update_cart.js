// document.addEventListener("DOMContentLoaded", function () {
//   // Attach event listeners to quantity increment/decrement buttons
//   document.querySelectorAll(".qtyBtn").forEach((button) => {
//     button.addEventListener("click", function (event) {
//       event.preventDefault();

//       const itemId = this.dataset.id; // Get item ID from data-id
//       const inputField = document.querySelector(
//         `.product-form__input[data-id='${itemId}']`
//       );
//       const totalField = document.querySelector(`#total-${itemId}`); // Item total field
//       const priceField = inputField
//         .closest("tr")
//         .querySelector(".cart__price-wrapper .money");
//       const pricePerUnit =
//         parseFloat(priceField.textContent.replace("$", "").trim()) || 0;

//       let quantity = parseInt(inputField.value) || 1;

//       // Adjust quantity based on button clicked
//       if (this.classList.contains("plus")) {
//         quantity++;
//       } else if (this.classList.contains("minus")) {
//         quantity = Math.max(1, quantity - 1);
//       }

//       inputField.value = quantity; // Update input field with new quantity

//       // Calculate and update total for this item
//       const totalPrice = pricePerUnit * quantity;
//       totalField.textContent = `$${totalPrice.toFixed(2)}`;

//       // Update subtotal for all items
//       updateSubtotal();

//       // Send updated cart data to the server
//       updateCartServer(itemId, quantity);
//     });
//   });

//   // Function to calculate and update the subtotal
//   function updateSubtotal() {
//     let subtotal = 0;
//     document.querySelectorAll(".cart-price .money").forEach((field) => {
//       const price = parseFloat(field.textContent.replace("$", "").trim()) || 0;
//       subtotal += price;
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }

//   // Function to send updated cart data to the server
//   function updateCartServer(itemId, quantity) {
//     const formData = new FormData();
//     formData.append("id", itemId);
//     formData.append("quantity", quantity);

//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken, // Include the CSRF token
//         "X-Requested-With": "XMLHttpRequest", // Identify this as AJAX request
//       },
//       body: formData,
//     })
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         if (data.success) {
//           console.log("Cart updated successfully");
//           updateCartUI(data.cart_items, data.subtotal);
//         } else {
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error:", error));
//   }

//   // Function to update the cart UI dynamically
//   function updateCartUI(cartItems, subtotal) {
//     cartItems.forEach((item) => {
//       const totalField = document.querySelector(`#total-${item.id}`);
//       if (totalField) {
//         totalField.textContent = `$${parseFloat(item.total_price.toFixed(2))}`;
//       }

//       const qtyField = document.querySelector(
//         `.product-form__input[data-id='${item.id}']`
//       );
//       if (qtyField) {
//         qtyField.value = item.quantity;
//       }
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${parseFloat(subtotal.toFixed(2))}`;
//     }
//   }

//   // Call updateSubtotal initially to ensure correct display on page load
//   updateSubtotal();
// });

// document.querySelectorAll(".qtyBtn").forEach((button) => {
//   button.addEventListener("click", (event) => {
//     event.preventDefault();

//     // Get the product ID from the data-id attribute
//     const itemId = button.getAttribute("data-id");

//     // Get the quantity input field for this item
//     const qtyField = document.querySelector(
//       `.product-form__input.qty[data-id='${itemId}']`
//     );

//     if (!qtyField) {
//       console.error(`Quantity field not found for item ID: ${itemId}`);
//       return;
//     }

//     // Determine if the button is for increasing or decreasing
//     const isPlus = button.classList.contains("plus");
//     let quantity = parseInt(qtyField.value) || 1;

//     // Update quantity
//     if (isPlus) {
//       quantity += 1;
//     } else if (quantity > 1) {
//       quantity -= 1;
//     }

//     qtyField.value = quantity;

//     // Find the total price field
//     const totalField = document.getElementById(`total-${itemId}`);
//     if (!totalField) {
//       console.error(`Total field not found for item ID: ${itemId}`);
//       return;
//     }

//     // Get the price per item
//     const pricePerItem = parseFloat(
//       totalField.textContent.replace("$", "") / quantity
//     );
//     if (isNaN(pricePerItem)) {
//       console.error(`Invalid price for item ID: ${itemId}`);
//       return;
//     }

//     // Update the total price for this item
//     const totalPrice = (pricePerItem * quantity).toFixed(2);
//     totalField.textContent = `$${totalPrice}`;

//     // Optionally, update the subtotal
//     const subtotalField = document.getElementById("subtotal");
//     if (subtotalField) {
//       let subtotal = 0;
//       document.querySelectorAll(".money[id^='total-']").forEach((field) => {
//         subtotal += parseFloat(field.textContent.replace("$", "")) || 0;
//       });
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     } else {
//       console.error("Subtotal field not found.");
//     }

//     // Optionally, send an AJAX request to update the backend
//     fetch(`/update-cart/${itemId}/`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": getCsrfToken(), // Ensure you have this function defined for CSRF tokens
//       },
//       body: JSON.stringify({ quantity }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         console.log(data);
//       })
//       .catch((error) => console.error(error));
//   });
// });

// document.querySelectorAll(".qtyBtn").forEach((button) => {
//   button.addEventListener("click", (event) => {
//     event.preventDefault();

//     const itemId = button.getAttribute("data-id");

//     const qtyField = document.querySelector(
//       `.product-form__input.qty[data-id='${itemId}']`
//     );

//     if (!qtyField) {
//       console.error(`Quantity field not found for item ID: ${itemId}`);
//       return;
//     }

//     const isPlus = button.classList.contains("plus");
//     let quantity = parseInt(qtyField.value) || 1;

//     if (isPlus) {
//       quantity += 1;
//     } else if (quantity > 1) {
//       quantity -= 1;
//     }

//     qtyField.value = quantity;

//     const totalField = document.getElementById(`total-${itemId}`);
//     if (!totalField) {
//       console.warn(`Total field not found for item ID: ${itemId}`);
//       return;
//     }

//     const pricePerItem = parseFloat(
//       totalField.textContent.replace("$", "") / quantity
//     );
//     if (isNaN(pricePerItem)) {
//       console.error(`Invalid price for item ID: ${itemId}`);
//       return;
//     }

//     const totalPrice = (pricePerItem * quantity).toFixed(2);
//     totalField.textContent = `$${totalPrice}`;

//     const subtotalField = document.getElementById("subtotal");
//     if (subtotalField) {
//       let subtotal = 0;
//       document.querySelectorAll(".money[id^='total-']").forEach((field) => {
//         subtotal += parseFloat(field.textContent.replace("$", "")) || 0;
//       });
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     } else {
//       console.error("Subtotal field not found.");
//     }

//     fetch(`/cart/${itemId}/`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": getCsrfToken(),
//       },
//       body: JSON.stringify({ quantity }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         console.log(data);
//       })
//       .catch((error) => console.error(error));
//   });
// });

// function getCsrfToken() {
//   const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
//   return csrfMetaTag ? csrfMetaTag.getAttribute("content") : null;
// }

// document.addEventListener("DOMContentLoaded", function () {
//   // Attach event listeners to quantity increment/decrement buttons
//   document.querySelectorAll(".qtyBtn").forEach((button) => {
//     button.addEventListener("click", function (event) {
//       event.preventDefault();

//       const itemId = this.dataset.id; // Get item ID from data-id
//       const inputField = document.querySelector(
//         `.product-form__input[data-id='${itemId}']`
//       );
//       const totalField = document.querySelector(`#total-${itemId}`); // Item total field
//       const priceField = inputField
//         .closest("tr")
//         .querySelector(".cart__price-wrapper .money");
//       const pricePerUnit =
//         parseFloat(priceField.textContent.replace("$", "").trim()) || 0;

//       let quantity = parseInt(inputField.value) || 1;

//       // Adjust quantity based on button clicked
//       if (this.classList.contains("plus")) {
//         quantity++;
//       } else if (this.classList.contains("minus")) {
//         quantity = Math.max(1, quantity - 1);
//       }

//       inputField.value = quantity; // Update input field with new quantity

//       // Calculate and update total for this item
//       const totalPrice = pricePerUnit * quantity;
//       totalField.textContent = `$${totalPrice.toFixed(2)}`;

//       // Update subtotal for all items
//       updateSubtotal();

//       // Send updated cart data to the server
//       updateCartServer(itemId, quantity);
//     });
//   });

//   // Function to calculate and update the subtotal
//   function updateSubtotal() {
//     let subtotal = 0;
//     document.querySelectorAll(".cart-price .money").forEach((field) => {
//       const price = parseFloat(field.textContent.replace("$", "").trim()) || 0;
//       subtotal += price;
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }

//   // Function to send updated cart data to the server
//   function updateCartServer(itemId, quantity) {
//     const formData = new FormData();
//     formData.append("id", itemId);
//     formData.append("quantity", quantity);

//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken, // Include the CSRF token
//         "X-Requested-With": "XMLHttpRequest", // Identify this as AJAX request
//       },
//       body: formData,
//     })
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         if (data.success) {
//           console.log("Cart updated successfully");
//           updateCartUI(data.cart_items, data.subtotal);
//         } else {
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error:", error));
//   }

//   // Function to update the cart UI dynamically
//   function updateCartUI(cartItems, subtotal) {
//     cartItems.forEach((item) => {
//       const totalField = document.querySelector(`#total-${item.id}`);
//       if (totalField) {
//         totalField.textContent = `$${parseFloat(item.total_price).toFixed(2)}`;
//       }

//       const qtyField = document.querySelector(
//         `.product-form__input[data-id='${item.id}']`
//       );
//       if (qtyField) {
//         qtyField.value = item.quantity;
//       }
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${parseFloat(subtotal).toFixed(2)}`;
//     }
//   }

//   // Call updateSubtotal initially to ensure correct display on page load
//   updateSubtotal();
// });

// document.addEventListener("DOMContentLoaded", function () {
//   // Function to update the subtotal dynamically
//   function updateSubtotal() {
//     let subtotal = 0;
//     document.querySelectorAll(".cart-price .money").forEach((field) => {
//       const price = parseFloat(field.textContent.replace("$", "").trim()) || 0;
//       subtotal += price;
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }

//   // Function to send updated cart data to the server
//   function updateCartServer(itemId, quantity) {
//     const formData = new FormData();
//     formData.append("id", itemId);
//     formData.append("quantity", quantity);

//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken, // Include the CSRF token
//         "X-Requested-With": "XMLHttpRequest", // Identify this as AJAX request
//       },
//       body: formData,
//     })
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         if (data.success) {
//           console.log("Cart updated successfully");
//           updateCartUI(data.cart_items, data.subtotal);
//         } else {
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error:", error));
//   }

//   // Function to update the cart UI dynamically
//   function updateCartUI(cartItems, subtotal) {
//     cartItems.forEach((item) => {
//       const totalField = document.querySelector(`#total-${item.id}`);
//       if (totalField) {
//         totalField.textContent = `$${parseFloat(item.total_price).toFixed(2)}`;
//       }

//       const qtyField = document.querySelector(
//         `.product-form__input[data-id='${item.id}']`
//       );
//       if (qtyField) {
//         qtyField.value = item.quantity;
//       }
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${parseFloat(subtotal).toFixed(2)}`;
//     }
//   }

//   // Attach event listeners to quantity increment/decrement buttons
//   document.querySelectorAll(".qtyBtn").forEach((button) => {
//     button.addEventListener("click", function (event) {
//       event.preventDefault();

//       const itemId = this.dataset.id || null; // Get item ID from data-id (if available)
//       const inputField = this.closest(".quantity-wrapper").querySelector(
//         ".product-form__input"
//       );
//       const totalField = document.querySelector(`#total-${itemId}`); // Item total field (cart page only)
//       const priceField = this.closest(
//         ".cart-item, .product-wrapper"
//       ).querySelector(".price-field .money");
//       const pricePerUnit =
//         parseFloat(priceField.textContent.replace("$", "").trim()) || 0;

//       let quantity = parseInt(inputField.value) || 1;

//       // Adjust quantity based on button clicked
//       if (this.classList.contains("plus")) {
//         quantity++;
//       } else if (this.classList.contains("minus")) {
//         quantity = Math.max(1, quantity - 1);
//       }

//       inputField.value = quantity; // Update input field with new quantity

//       // Update total price for cart page
//       if (totalField) {
//         const totalPrice = pricePerUnit * quantity;
//         totalField.textContent = `$${totalPrice.toFixed(2)}`;
//       }

//       // Update subtotal (for cart page only)
//       if (document.querySelector(".cart-page")) {
//         updateSubtotal();
//       }

//       // Update the server with the new quantity (only for cart page)
//       if (itemId) {
//         updateCartServer(itemId, quantity);
//       }
//     });
//   });

//   // Call updateSubtotal initially to ensure correct display on page load (for cart page)
//   if (document.querySelector(".cart-page")) {
//     updateSubtotal();
//   }
// });

// document.addEventListener("DOMContentLoaded", function () {
//   // Function to update the subtotal dynamically
//   function updateSubtotal() {
//     let subtotal = 0;
//     document.querySelectorAll(".cart-price .money").forEach((field) => {
//       const price = parseFloat(field.textContent.replace("$", "").trim()) || 0;
//       subtotal += price;
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }

//   // Function to send updated cart data to the server
//   function updateCartServer(itemId, quantity) {
//     const formData = new FormData();
//     formData.append("id", itemId);
//     formData.append("quantity", quantity);

//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken, // Include the CSRF token
//         "X-Requested-With": "XMLHttpRequest", // Identify this as AJAX request
//       },
//       body: formData,
//     })
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         if (data.success) {
//           console.log("Cart updated successfully");
//           updateCartUI(data.cart_items, data.subtotal);
//         } else {
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error:", error));
//   }

//   // Function to update the cart UI dynamically
//   function updateCartUI(cartItems, subtotal) {
//     cartItems.forEach((item) => {
//       const totalField = document.querySelector(`#total-${item.id}`);
//       if (totalField) {
//         totalField.textContent = `$${parseFloat(item.total_price).toFixed(2)}`;
//       }

//       const qtyField = document.querySelector(
//         `.product-form__input[data-id='${item.id}']`
//       );
//       if (qtyField) {
//         qtyField.value = item.quantity;
//       }
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${parseFloat(subtotal).toFixed(2)}`;
//     }
//   }

//   // Attach event listeners to quantity increment/decrement buttons
//   document.querySelectorAll(".qtyBtn").forEach((button) => {
//     button.addEventListener("click", function (event) {
//       event.preventDefault();

//       const itemId = this.dataset.id || null; // Get item ID from data-id (if available)
//       const inputField = this.closest(".quantity-wrapper")?.querySelector(
//         ".product-form__input"
//       );
//       if (!inputField) {
//         console.error("Input field not found");
//         return;
//       }

//       const priceField = this.closest(
//         ".cart-item, .product-wrapper"
//       )?.querySelector(".price-field .money");
//       if (!priceField) {
//         console.error("Price field not found");
//         return;
//       }

//       const totalField = document.querySelector(`#total-${itemId}`); // Item total field (cart page only)
//       const pricePerUnit =
//         parseFloat(priceField.textContent.replace("$", "").trim()) || 0;

//       let quantity = parseInt(inputField.value) || 1;

//       // Adjust quantity based on button clicked
//       if (this.classList.contains("plus")) {
//         quantity++;
//       } else if (this.classList.contains("minus")) {
//         quantity = Math.max(1, quantity - 1);
//       }

//       inputField.value = quantity; // Update input field with new quantity

//       // Update total price for cart page
//       if (totalField) {
//         const totalPrice = pricePerUnit * quantity;
//         totalField.textContent = `$${totalPrice.toFixed(2)}`;
//       }

//       // Update subtotal (for cart page only)
//       if (document.querySelector(".cart-page")) {
//         updateSubtotal();
//       }

//       // Update the server with the new quantity (only for cart page)
//       if (itemId) {
//         updateCartServer(itemId, quantity);
//       }
//     });
//   });

//   // Call updateSubtotal initially to ensure correct display on page load (for cart page)
//   if (document.querySelector(".cart-page")) {
//     updateSubtotal();
//   }
// });

// document.addEventListener("DOMContentLoaded", function () {
//   // Attach event listeners to quantity increment/decrement buttons
//   document.querySelectorAll(".qtyBtn").forEach((button) => {
//     button.addEventListener("click", function (event) {
//       event.preventDefault();

//       const itemId = this.dataset.id; // Get item ID from data-id
//       const isCartPage = this.closest(".cart__qty") !== null; // Determine if it's the cart page
//       const qtyFieldSelector = isCartPage
//         ? `.product-form__input[data-id='${itemId}']`
//         : "#Quantity";
//       const priceSelector = isCartPage
//         ? ".cart__price-wrapper .money"
//         : ".product-form__price .money";

//       // Locate the quantity input field
//       const inputField = document.querySelector(qtyFieldSelector);
//       if (!inputField) {
//         console.error("Input field not found:", { itemId, button: this });
//         return;
//       }

//       // Locate the price field (cart page or product page)
//       const priceField = this.closest(
//         "tr, .product-form__item--quantity"
//       )?.querySelector(priceSelector);
//       if (!priceField) {
//         console.error("Price field not found:", { itemId, button: this });
//         return;
//       }

//       const totalField = isCartPage
//         ? document.querySelector(`#total-${itemId}`)
//         : null; // Only for the cart page
//       const pricePerUnit =
//         parseFloat(priceField.textContent.replace("$", "").trim()) || 0;

//       let quantity = parseInt(inputField.value) || 1;

//       // Adjust quantity based on button clicked
//       if (this.classList.contains("plus")) {
//         quantity++;
//       } else if (this.classList.contains("minus")) {
//         quantity = Math.max(1, quantity - 1);
//       }

//       inputField.value = quantity; // Update input field with new quantity

//       // Update total price for the cart page
//       if (isCartPage && totalField) {
//         const totalPrice = pricePerUnit * quantity;
//         totalField.textContent = `$${totalPrice.toFixed(2)}`;
//       }

//       // Update subtotal (cart page only)
//       if (isCartPage) {
//         updateSubtotal();
//         updateCartServer(itemId, quantity);
//       }
//     });
//   });

//   // Function to calculate and update the subtotal (cart page only)
//   function updateSubtotal() {
//     let subtotal = 0;
//     document
//       .querySelectorAll(".cart__price-wrapper .money")
//       .forEach((field) => {
//         const price =
//           parseFloat(field.textContent.replace("$", "").trim()) || 0;
//         subtotal += price;
//       });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }

//   // Function to send updated cart data to the server
//   function updateCartServer(itemId, quantity) {
//     const formData = new FormData();
//     formData.append("id", itemId);
//     formData.append("quantity", quantity);

//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken,
//         "X-Requested-With": "XMLHttpRequest",
//       },
//       body: formData,
//     })
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         if (data.success) {
//           console.log("Cart updated successfully");
//           updateCartUI(data.cart_items, data.subtotal);
//         } else {
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error:", error));
//   }

//   // Function to update the cart UI dynamically
//   function updateCartUI(cartItems, subtotal) {
//     cartItems.forEach((item) => {
//       const totalField = document.querySelector(`#total-${item.id}`);
//       if (totalField) {
//         totalField.textContent = `$${parseFloat(item.total_price).toFixed(2)}`;
//       }

//       const qtyField = document.querySelector(
//         `.product-form__input[data-id='${item.id}']`
//       );
//       if (qtyField) {
//         qtyField.value = item.quantity;
//       }
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${parseFloat(subtotal).toFixed(2)}`;
//     }
//   }

//   // Initialize the subtotal calculation (cart page only)
//   if (document.querySelector(".cart__qty")) {
//     updateSubtotal();
//   }
// });

// document.addEventListener("DOMContentLoaded", function () {
//   document.querySelectorAll(".qtyBtn").forEach((button) => {
//     button.addEventListener("click", function (event) {
//       event.preventDefault();

//       const itemId = this.dataset.id; // Get item ID from data-id
//       if (!itemId) {
//         console.error("Item ID is missing:", { button: this });
//         return;
//       }

//       const isCartPage = this.closest(".cart__qty") !== null;
//       const qtyFieldSelector = isCartPage
//         ? `.product-form__input[data-id='${itemId}']`
//         : "#Quantity-${itemId}";
//       const inputField = document.querySelector(qtyFieldSelector);

//       if (!inputField) {
//         console.error("Quantity input field not found for item:", { itemId });
//         return;
//       }

//       let quantity = parseInt(inputField.value) || 1;

//       if (this.classList.contains("plus")) {
//         quantity++;
//       } else if (this.classList.contains("minus")) {
//         quantity = Math.max(1, quantity - 1);
//       }

//       inputField.value = quantity;
//       updateCartServer(itemId, quantity); // Send to server
//     });
//   });

//   function updateCartServer(itemId, quantity) {
//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken,
//         "X-Requested-With": "XMLHttpRequest",
//       },
//       body: new URLSearchParams({ id: itemId, quantity: quantity }),
//     })
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Network response was not ok");
//         }
//         return response.json();
//       })
//       .then((data) => {
//         if (data.success) {
//           console.log("Cart updated successfully");
//           // Update UI logic here
//         } else {
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error syncing cart:", error));
//   }
// });

document.addEventListener("DOMContentLoaded", function () {
  // Attach event listeners to quantity increment/decrement buttons
  document.querySelectorAll(".qtyBtn").forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault();

      const itemId = this.dataset.id; // Get item ID from data-id
      if (!itemId) {
        console.error("Item ID is missing:", { button: this });
        return;
      }

      // Determine if the action is on the cart page or product page
      const isCartPage = this.closest(".cart__qty") !== null;

      // Select the quantity input field
      const qtyFieldSelector = isCartPage
        ? `.product-form__input[data-id='${itemId}']`
        : `#Quantity-${itemId}`; // Adjusted for product page
      const inputField = document.querySelector(qtyFieldSelector);

      if (!inputField) {
        console.error("Quantity input field not found for item:", { itemId });
        return;
      }

      // Get the current quantity and update based on button clicked
      let quantity = parseInt(inputField.value) || 1;
      if (this.classList.contains("plus")) {
        quantity++;
      } else if (this.classList.contains("minus")) {
        quantity = Math.max(1, quantity - 1);
      }

      inputField.value = quantity; // Update the input field value

      // Send the updated quantity to the server
      updateCartServer(itemId, quantity);
    });
  });

  // Function to send updated cart data to the server
  function updateCartServer(itemId, quantity) {
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    fetch("/shop/cart/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: new URLSearchParams({ id: itemId, quantity: quantity }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          console.log("Cart updated successfully");

          // Update UI dynamically if on cart page
          if (document.querySelector(".cart__qty")) {
            updateCartUI(data.cart_items, data.subtotal);
          }
        } else {
          alert("Error updating cart. Please try again.");
        }
      })
      .catch((error) => console.error("Error syncing cart:", error));
  }

  // Function to update the cart UI dynamically (cart page only)
  function updateCartUI(cartItems, subtotal) {
    cartItems.forEach((item) => {
      const totalField = document.querySelector(`#total-${item.id}`);
      if (totalField) {
        totalField.textContent = `$${parseFloat(item.total_price).toFixed(2)}`;
      }

      const qtyField = document.querySelector(
        `.product-form__input[data-id='${item.id}']`
      );
      if (qtyField) {
        qtyField.value = item.quantity;
      }
    });

    const subtotalField = document.querySelector("#subtotal");
    if (subtotalField) {
      subtotalField.textContent = `$${parseFloat(subtotal).toFixed(2)}`;
    }
  }
});
