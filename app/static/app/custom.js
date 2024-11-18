// (function ($) {
//     'use strict';

//     // Function to initialize the Slick Slider
//     function product_slider() {
//         // Initialize the slider
//         $('.productSlider').slick({
//             dots: false,         // Remove dots navigation
//             infinite: true,      // Infinite loop of slides
//             slidesToShow: 4,     // Number of products to show at once
//             slidesToScroll: 1,   // Scroll 1 product at a time
//             arrows: true,        // Enable arrows for navigation
//             responsive: [
//                 {
//                     breakpoint: 1024,
//                     settings: {
//                         slidesToShow: 3,
//                         slidesToScroll: 1
//                     }
//                 },
//                 {
//                     breakpoint: 600,
//                     settings: {
//                         slidesToShow: 2,
//                         slidesToScroll: 1
//                     }
//                 },
//                 {
//                     breakpoint: 480,
//                     settings: {
//                         slidesToShow: 1,
//                         slidesToScroll: 1
//                     }
//                 }
//             ]
//         });
//     }

//     // Trigger the Slick slider initialization when the document is ready
//     $(document).ready(function () {
//         // Ensure the productSlider is initialized correctly
//         product_slider();
//     });

//     // Re-initialize the slider on window resize or after dynamic content loading
//     $(window).on('resize', function() {
//         $('.productSlider').slick('setPosition');
//     });

// })(jQuery);

