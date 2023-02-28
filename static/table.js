function send_value(index, column, value) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './change_table');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('index=' + index + '&column=' + column + '&value=' + value);
}

function cell_context_menu() {
    context_menu = document.getElementById('context-menu');
    context_menu.style.display = 'block';
    context_menu.style.top = window.event.clientY + 'px';
    context_menu.style.left = window.event.clientX + 'px';
    window.event.preventDefault();
}