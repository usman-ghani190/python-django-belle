// $(document).ready(function () {
//     $('.qtyBtn plus').click(function (e) { 
//         e.preventDefault();

//         var inc_value = $(this).closest('.qtyField').find('.input qty').val();
//         var value = parseInt(inc_value, 10);
//         value= isNaN(value) ? 0: value;

//         if(value < 10)
//         {
//             value++;
//             $(this).closest('.qtyField').find('.input qty').val(value);
//         }
        
//     });
// });

$(document).ready(function () {
    // Increment Quantity
    $('.qtyBtn.plus').click(function (e) {
        e.preventDefault();

        var $input = $(this).closest('.qtyField').find('.qty');
        var value = parseInt($input.val(), 10);
        value = isNaN(value) ? 0 : value;

        if (value < 10) {
            value++;
            $input.val(value);
        }
    });

    // Decrement Quantity
    $('.qtyBtn.minus').click(function (e) {
        e.preventDefault();

        var $input = $(this).closest('.qtyField').find('.qty');
        var value = parseInt($input.val(), 10);
        value = isNaN(value) ? 0 : value;

        if (value > 1) {
            value--;
            $input.val(value);
        }
    });
});
