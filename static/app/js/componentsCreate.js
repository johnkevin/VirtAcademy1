$(function () {
    function createCell(text) {
        var td = document.createElement('td');
        if (text) { td.innerText = text; }
        return td;
    }
    function formartDate(date) {
        if (date.trim() == '' || date == null || (typeof date == "undefined")) {
            return '';
        } else {
            var year = date.substr(0, 4);
            var month = date.substr(5, 2);
            var day = date.substr(8, 2);
            return [day, month, year].join('-');
        }
    }
    function formatString(valor) {
        if (valor == null || (typeof valor == "undefined"))
            return '';
        else
            return valor;
    }
    function createCell_aux(text) {
        var td = document.createElement('td');
        if (text) { td.innerHTML = text; }
        return td;
    }
    
});


