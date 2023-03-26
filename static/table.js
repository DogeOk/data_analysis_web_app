//Send values to server for changing them in the table
function sendValue(object) {
    index = object.getAttribute('index');
    column = object.getAttribute('column');
    value = object.value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './table/change_table');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('index=' + index + '&column=' + column + '&value=' + value);
}

//Create cell context menu
function cellContextMenu(object) {
    createContextMenu(['Удалить столбец', 'Удалить строку'], [
        function deleteColumn() {
            column = object.getAttribute('column');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', './table/delete_column');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    location.reload();
                }
            }
            xhr.send('column=' + column);
        },
        function deleteRow() {
            index = object.getAttribute('index');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', './table/delete_row');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    location.reload();
                }
            }
            xhr.send('index=' + index);
        },
    ]);
    window.event.preventDefault();
}

//Create column context menu
function columnContextMenu(object) {
    createContextMenu([
        'Удалить столбец',
        'Удалить строки с пропусками',
        'Уникальные значения столбца',
        'Заменить значения',
    ], [
        function deleteColumn() {
            column = object.getAttribute('column');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', './table/delete_column');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    location.reload();
                }
            }
            xhr.send('column=' + column);
        },
        function deleteSkips() {
            column = object.getAttribute('column');
            var check = new XMLHttpRequest();
            check.open('POST', './table/check_skips');
            check.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            check.onreadystatechange = function() {
                if (check.readyState === 4 && check.status === 200) {
                    if (confirm('Данное действие затронет ' + check.responseText + ' строк. Продолжить?')) {
                        var xhr = new XMLHttpRequest();
                        xhr.open('POST', './table/delete_skips');
                        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        xhr.onreadystatechange = function() {
                            if (xhr.readyState === 4 && xhr.status === 200) {
                                location.reload();
                            }
                        }
                        xhr.send('column=' + column);
                    }
                }
            }
            check.send('column=' + column);
        },
        function uniqueValues() {
            column = object.getAttribute('column');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', './table/unique_values');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    document.getElementById('infoModalLabel').innerText = 'Уникальные значения столбца ' + column;
                    document.getElementById('infoText').innerText = xhr.responseText;
                    bootstrap.Modal.getOrCreateInstance(document.getElementById('infoModal')).show()
                }
            }
            xhr.send('column=' + column);
        },
        function replaceValues() {
            column = object.getAttribute('column');
            document.getElementById('replaceModalLabel').innerText = 'Заменить значения в столбце ' + column;
            document.getElementById('columnReplace').value = column;
            bootstrap.Modal.getOrCreateInstance(document.getElementById('replaceModal')).show()
        }
    ]);
    window.event.preventDefault();
}

// Delete duplicates
function deleteDuplicates(column) {
    var xhr = new XMLHttpRequest();
    var check = new XMLHttpRequest();
    check.open('POST', './table/check_duplicates');
    check.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    check.onreadystatechange = function() {
        if (check.readyState === 4 && check.status === 200) {
            if (confirm('Данное действие затронет ' + check.responseText + ' строк. Продолжить?')) {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', './table/delete_duplicates');
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        location.reload();
                    }
                }
                xhr.send('column=' + column);
            }
        }
    }
    check.send('column=' + column);
}

function getTableInfo() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', './table/table_info');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('infoModalLabel').innerText = 'Общая информация о таблице';
            document.getElementById('infoText').innerText = xhr.responseText;
            bootstrap.Modal.getOrCreateInstance(document.getElementById('infoModal')).show()
        }
    }
    xhr.send('');
}

function getTableSkips() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './table/check_skips');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('infoModalLabel').innerText = 'Количество пропусков в таблице';
            document.getElementById('infoText').innerText = xhr.responseText;
            bootstrap.Modal.getOrCreateInstance(document.getElementById('infoModal')).show()
        }
    }
    xhr.send('column=:');
}
