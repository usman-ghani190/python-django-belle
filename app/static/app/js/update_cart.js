document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = "{{ csrf_token }}";

    // Add event listeners for quantity buttons
    document.querySelectorAll('.qtyBtn').forEach(button => {
        button.addEventListener('click', function() {
            let action = this.classList.contains('minus') ? -1 : 1;
            let inputField = this.closest('.qtyField').querySelector('input');
            let newQuantity = parseInt(inputField.value) + action;
            let itemId = this.dataset.id;

            if (newQuantity >= 1) {
                updateQuantity(itemId, newQuantity, inputField);
            }
        });
    });

    function updateQuantity(itemId, quantity, inputField) {
        fetch("{% url 'cart' %}", {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
            body: new URLSearchParams({
                'update_quantity': 'true',
                'item_id': itemId,
                'quantity': quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            inputField.value = quantity;

            // Update totals on the cart page
            if (document.getElementById(`total-${itemId}`)) {
                document.getElementById(`total-${itemId}`).innerText = data.total_price.toFixed(2);
                document.getElementById('subtotal').innerText = data.subtotal.toFixed(2);
            }

            // Update totals on the product detail page
            if (document.getElementById('product-total')) {
                document.getElementById('product-total').innerText = data.total_price.toFixed(2);
            }
        });
    }
});
