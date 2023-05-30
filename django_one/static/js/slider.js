
var dateSlider = document.getElementById('slider-date');

function timestamp(str) {
    return new Date(str).getTime();
}


var maxDate = new Date().getFullYear();

var slider = noUiSlider.create(dateSlider, {

    start: [1970, maxDate],
    step:1,
    connect: true,
    tooltips: true,
    range: {
        'min': 1900,
        'max': maxDate
    },
    format: wNumb( { decimals: 0 })
});

$("#min-max").val(slider.get());

//update hidden input value on slider change
slider.on("change", function() {
    $("#min-max").val(slider.get());
});
