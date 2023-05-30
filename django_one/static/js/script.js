const rating = document.querySelector('form[name=rating]');

if(rating){
    rating.addEventListener("change", function (e) {
        // Получаем данные из формы
        let data = new FormData(this);
        fetch(`${this.action}`, {
            method: 'POST',
            body: data
        })
    });
}
