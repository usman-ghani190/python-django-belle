// document.addEventListener("DOMContentLoaded", function () {
//   attachCartEventListeners();

//   function attachCartEventListeners() {
//     // Attach event listeners for quantity increment/decrement
//     document.querySelectorAll(".qtyBtn").forEach((button) => {
//       button.addEventListener("click", function (event) {
//         event.preventDefault();

//         const itemId = this.dataset.id; // Get item ID from data-id
//         if (!itemId) {
//           console.error("Item ID is missing:", { button: this });
//           return;
//         }

//         // Identify if we're on the cart page or mini-cart
//         const isCartPage = this.closest(".cart__qty") !== null;
//         const isMiniCart = this.closest(".mini-products-list") !== null;

//         // Identify the appropriate input field
//         const qtyField = document.querySelector(
//           isCartPage
//             ? `.product-form__input[data-id='${itemId}']`
//             : `#Quantity-${itemId}`
//         );

//         if (!qtyField) {
//           console.error("Quantity input field not found for item:", { itemId });
//           return;
//         }

//         // Get current quantity and update it based on button action
//         let quantity = parseInt(qtyField.value) || 1;
//         if (this.classList.contains("plus")) {
//           quantity++;
//         } else if (this.classList.contains("minus")) {
//           quantity = Math.max(1, quantity - 1);
//         }

//         // Update the quantity field
//         qtyField.value = quantity;

//         // Send updated quantity to the server
//         updateCartServer(itemId, quantity);
//       });
//     });

//     // Attach event listeners for remove buttons
//     document.querySelectorAll(".remove").forEach((button) => {
//       button.addEventListener("click", function (event) {
//         event.preventDefault();

//         const itemId = this.dataset.id; // Get item ID from data-id
//         if (!itemId) {
//           console.error("Item ID is missing for removal:", { button: this });
//           return;
//         }

//         // Send a request to remove the item
//         removeItemFromCart(itemId);
//       });
//     });
//   }

//   // Function to update cart on the server
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
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.success) {
//           // Update both cart page and mini-cart dynamically
//           updateCartUI(data.cart_items, data.subtotal);
//           updateMiniCartUI(data.cart_items, data.subtotal);
//         } else {
//           console.error("Error updating cart:", data.error);
//           alert("Error updating cart. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error syncing cart:", error));
//   }

//   // Function to remove an item from the cart
//   function removeItemFromCart(itemId) {
//     const csrfToken = document.querySelector(
//       "[name=csrfmiddlewaretoken]"
//     ).value;

//     fetch("/shop/cart/", {
//       method: "POST",
//       headers: {
//         "X-CSRFToken": csrfToken,
//         "X-Requested-With": "XMLHttpRequest",
//       },
//       body: new URLSearchParams({ id: itemId, action: "remove" }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.success) {
//           // Update UI dynamically
//           updateCartUI(data.cart_items, data.subtotal);
//           updateMiniCartUI(data.cart_items, data.subtotal);
//         } else {
//           console.error("Error removing item:", data.error);
//           alert("Error removing item. Please try again.");
//         }
//       })
//       .catch((error) => console.error("Error removing item:", error));
//   }

//   // Function to update the cart page UI dynamically
//   function updateCartUI(cartItems, subtotal) {
//     cartItems.forEach((item) => {
//       const totalField = document.querySelector(`#total-${item.id}`);
//       if (totalField) {
//         totalField.textContent = `$${item.total_price.toFixed(2)}`;
//       }

//       const qtyField = document.querySelector(`#Quantity-${item.id}`);
//       if (qtyField) {
//         qtyField.value = item.quantity; // Update the quantity field
//       }
//     });

//     const subtotalField = document.querySelector("#subtotal");
//     if (subtotalField) {
//       subtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }

//   // Function to update the mini-cart UI dynamically
//   function updateMiniCartUI(cartItems, subtotal) {
//     const miniCartList = document.querySelector(".mini-products-list");
//     if (miniCartList) {
//       // Clear current items and re-render
//       miniCartList.innerHTML = "";
//       cartItems.forEach((item) => {
//         miniCartList.innerHTML += `
//           <li class="item">
//             <a class="product-image" href="#">
//               <img src="${item.product.image_url}" alt="${item.product.name}">
//             </a>
//             <div class="product-details">
//               <a href="#" class="remove" data-id="${
//                 item.id
//               }"><i class="anm anm-times-l" aria-hidden="true"></i></a>
//               <a class="pName" href="#">${item.product.name}</a>
//               <div class="wrapQtyBtn">
//                 <div class="qtyField">
//                   <span class="label">Qty:</span>
//                   <a class="qtyBtn minus" href="javascript:void(0);" data-id="${
//                     item.id
//                   }"><i class="fa anm anm-minus-r" aria-hidden="true"></i></a>
//                   <input type="text" id="Quantity-${
//                     item.id
//                   }" name="quantity" value="${
//           item.quantity
//         }" class="product-form__input qty">
//                   <a class="qtyBtn plus" href="javascript:void(0);" data-id="${
//                     item.id
//                   }"><i class="fa anm anm-plus-r" aria-hidden="true"></i></a>
//                 </div>
//               </div>
//               <div class="priceRow">
//                 <div class="product-price">
//                   <span class="money">$${item.total_price.toFixed(2)}</span>
//                 </div>
//               </div>
//             </div>
//           </li>`;
//       });

//       // Re-attach event listeners for newly rendered items
//       attachCartEventListeners();
//     }

//     const miniCartSubtotalField = document.querySelector(
//       "#header-cart .total .money"
//     );
//     if (miniCartSubtotalField) {
//       miniCartSubtotalField.textContent = `$${subtotal.toFixed(2)}`;
//     }
//   }
// });

document.addEventListener("DOMContentLoaded", function () {
  attachCartEventListeners();

  function attachCartEventListeners() {
    // Attach event listeners for quantity increment/decrement
    document.querySelectorAll(".qtyBtn").forEach((button) => {
      button.addEventListener("click", function (event) {
        event.preventDefault();

        const itemId = this.dataset.id; // Get item ID from data-id
        if (!itemId) {
          console.error("Item ID is missing:", { button: this });
          return;
        }

        // Identify if we're on the cart page or mini-cart
        const isCartPage = this.closest(".cart__qty") !== null;
        const isMiniCart = this.closest(".mini-products-list") !== null;

        // Identify the appropriate input field
        const qtyField = document.querySelector(
          isCartPage
            ? `.product-form__input[data-id='${itemId}']`
            : `#Quantity-${itemId}`
        );

        if (!qtyField) {
          console.error("Quantity input field not found for item:", { itemId });
          return;
        }

        // Get current quantity and update it based on button action
        let quantity = parseInt(qtyField.value) || 1;
        if (this.classList.contains("plus")) {
          quantity++;
        } else if (this.classList.contains("minus")) {
          quantity = Math.max(1, quantity - 1);
        }

        // Update the quantity field
        qtyField.value = quantity;

        // Send updated quantity to the server
        updateCartServer(itemId, quantity);
      });
    });

    // Attach event listeners for remove buttons
    document.querySelectorAll(".remove").forEach((button) => {
      button.addEventListener("click", function (event) {
        event.preventDefault();

        const itemId = this.dataset.id; // Get item ID from data-id
        if (!itemId) {
          console.error("Item ID is missing for removal:", { button: this });
          return;
        }

        // Send a request to remove the item
        removeItemFromCart(itemId);
      });
    });
  }

  // Function to update cart count dynamically
  function updateCartCount(cartCount) {
    const cartCountElement = document.getElementById("CartCount");
    if (cartCountElement) {
      cartCountElement.textContent = cartCount; // Update the cart count
    }
  }

  // Function to update cart on the server
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
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Update both cart page and mini-cart dynamically
          updateCartUI(data.cart_items, data.subtotal);
          updateMiniCartUI(data.cart_items, data.subtotal);
          updateCartCount(data.cart_count); // Update the cart count
        } else {
          console.error("Error updating cart:", data.error);
          alert("Error updating cart. Please try again.");
        }
      })
      .catch((error) => console.error("Error syncing cart:", error));
  }

  // Function to remove an item from the cart
  function removeItemFromCart(itemId) {
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    fetch("/shop/cart/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: new URLSearchParams({ id: itemId, action: "remove" }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Update UI dynamically
          updateCartUI(data.cart_items, data.subtotal);
          updateMiniCartUI(data.cart_items, data.subtotal);
          updateCartCount(data.cart_count); // Update the cart count
        } else {
          console.error("Error removing item:", data.error);
          alert("Error removing item. Please try again.");
        }
      })
      .catch((error) => console.error("Error removing item:", error));
  }

  // Function to update the cart page UI dynamically
  function updateCartUI(cartItems, subtotal) {
    cartItems.forEach((item) => {
      const totalField = document.querySelector(`#total-${item.id}`);
      if (totalField) {
        totalField.textContent = `$${item.total_price.toFixed(2)}`;
      }

      const qtyField = document.querySelector(`#Quantity-${item.id}`);
      if (qtyField) {
        qtyField.value = item.quantity; // Update the quantity field
      }
    });

    const subtotalField = document.querySelector("#subtotal");
    if (subtotalField) {
      subtotalField.textContent = `$${subtotal.toFixed(2)}`;
    }
  }

  // Function to update the mini-cart UI dynamically
  function updateMiniCartUI(cartItems, subtotal) {
    const miniCartList = document.querySelector(".mini-products-list");
    if (miniCartList) {
      // Clear current items and re-render
      miniCartList.innerHTML = "";
      cartItems.forEach((item) => {
        miniCartList.innerHTML += `
          <li class="item">
            <a class="product-image" href="#">
              <img src="${item.product.image_url}" alt="${item.product.name}">
            </a>
            <div class="product-details">
              <a href="#" class="remove" data-id="${
                item.id
              }"><i class="anm anm-times-l" aria-hidden="true"></i></a>
              <a class="pName" href="#">${item.product.name}</a>
              <div class="wrapQtyBtn">
                <div class="qtyField">
                  <span class="label">Qty:</span>
                  <a class="qtyBtn minus" href="javascript:void(0);" data-id="${
                    item.id
                  }"><i class="fa anm anm-minus-r" aria-hidden="true"></i></a>
                  <input type="text" id="Quantity-${
                    item.id
                  }" name="quantity" value="${
          item.quantity
        }" class="product-form__input qty">
                  <a class="qtyBtn plus" href="javascript:void(0);" data-id="${
                    item.id
                  }"><i class="fa anm anm-plus-r" aria-hidden="true"></i></a>
                </div>
              </div>
              <div class="priceRow">
                <div class="product-price">
                  <span class="money">$${item.total_price.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </li>`;
      });

      // Re-attach event listeners for newly rendered items
      attachCartEventListeners();
    }

    const miniCartSubtotalField = document.querySelector(
      "#header-cart .total .money"
    );
    if (miniCartSubtotalField) {
      miniCartSubtotalField.textContent = `$${subtotal.toFixed(2)}`;
    }
  }
});
