const choices = new Choices('[data-trigger]',
      {
        searchEnabled: false,
        itemSelectText: '',
      });
//Setings for datespicker
flatpickr(".datepicker", {
    dateFormat: "m/d/y",
    minDate: "today"
});
var btnTypes = document.querySelectorAll('.travel-type-wrap .item')
var mainForm = document.getElementById('main-form')
for (let i = 0; i < btnTypes.length; i++) {
    btnTypes[i].addEventListener('click', function() {
        for (let i = 0; i < btnTypes.length; i++) {
            btnTypes[i].classList.remove('active')
        }
        btnTypes[i].classList.add('active')
        let className = 'type' + i
        mainForm.className = `${className} main-form`
    })
}
//Setings for timepicker
flatpickr(".timepicker", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true
});
var btnTypes = document.querySelectorAll('.travel-type-wrap .item')
var mainForm = document.getElementById('main-form')
for (let i = 0; i < btnTypes.length; i++) {
    btnTypes[i].addEventListener('click', function() {
        for (let i = 0; i < btnTypes.length; i++) {
            btnTypes[i].classList.remove('active')
        }
        btnTypes[i].classList.add('active')
        let className = 'type' + i
        mainForm.className = `${className} main-form`
    })
}