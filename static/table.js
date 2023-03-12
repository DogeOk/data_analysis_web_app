function sendValue(index, column, value) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './table/change_table');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('index=' + index + '&column=' + column + '&value=' + value);
}

function cellContextMenu() {
    createContextMenu(['test', 'test2'], ['test']);
    window.event.preventDefault();
}
