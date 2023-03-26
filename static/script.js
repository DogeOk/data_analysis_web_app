// Hide context menu on left click
document.addEventListener('click', function() {
    context_menu = document.getElementById('context-menu');
    context_menu.style.display = 'none';
}, false);

// Hide default context menu on right click
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
}, false);

// Create context menu with elements and actions
function createContextMenu(elements, functions, object) {
    context_menu = document.getElementById('context-menu');
    context_menu.innerHTML = '';
    context_menu.style.display = 'block';
    context_menu.style.top = window.event.clientY + 'px';
    context_menu.style.left = window.event.clientX + 'px';
    for (var i = 0; i < elements.length; i++) {
        element = document.createElement('a');
        element.className = "dropdown-item";
        element.textContent = elements[i];
        element.href = "#";
        element.onclick = functions[i];
        context_menu.appendChild(element);
    }
}

// Hide one element and show another element
function hideShow(hideBlock, showBlock) {
    document.getElementById(hideBlock).style.display = 'none';
    document.getElementById(showBlock).style.display = 'block';
}

// Variables for check login and password
bad_login = false;
bad_password = false;

// Check login and show feedback
function checkLogin(login) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './check_login');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200){
            if (xhr.responseText != 'None') {
                document.getElementById('invalidLogin').style.display = 'block';
                window.bad_login = true;
            } else {
                document.getElementById('invalidLogin').style.display = 'none';
                window.bad_login = false;
            }
        }
    }
    xhr.send('login=' + login);
}

// Check passwords on repeat and show feedback
function checkPassword() {
    password = document.getElementById('inputRegisterPassword').value;
    repeat_password = document.getElementById('inputRepeatPassword').value;
    if (password != '' && repeat_password != '') {
        if (password == repeat_password) {
            document.getElementById('invalidPassword').style.display = 'none';
            window.bad_password = false;
        } else {
            document.getElementById('invalidPassword').style.display = 'block';
            window.bad_password = true;
        }
    }
}

// Send values to server for adding account
function addAccount() {
    login = document.getElementById('inputRegisterLogin').value;
    password = document.getElementById('inputRegisterPassword').value;
    if (window.bad_login) {
        alert('Такой логин уже существует.');
        return;
    }
    if (window.bad_password) {
        alert('Пароли не совпадают.');
        return;
    }
    if (login == '') {
        alert('Поле для логина пустует.');
        return;
    }
    if (password == '') {
        alert('Поле для пароля пустует');
        return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './add_account');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200){
            if (xhr.responseText == 'Success') {
                location.reload();
            } else {
                alert('Простите. При регистрации что-то пошло не так.');
            }
        }
    }
    xhr.send('login=' + login + '&password=' + password);
}

// Authorization
function login() {
    login = document.getElementById('inputLogin').value;
    password = document.getElementById('inputPassword').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './login');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200){
            if (xhr.responseText == 'Success') {
                location.reload();
            } else {
                alert('Неверный логин или пароль.');
            }
        }
    }
    xhr.send('login=' + login + '&password=' + password);
}

// Get all user files
function getUserFiles() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', './user_files');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200){
            file_elements = document.querySelectorAll('.file');
            for (let index = 0; index < file_elements.length; index++) {
                file_elements[index].remove();
            }
            files = JSON.parse(xhr.responseText);
            files_window = document.getElementById('filesWindow');
            for (let index = 0; index < files.length; index++) {
                file = document.createElement('div');
                file.className = 'file';
                file.setAttribute('onclick', 'openFile(this);');
                file.setAttribute('file-name', files[index]);
                file.setAttribute('selected', false);
                file_icon = document.createElement('div');
                file_icon.className = 'file-icon';
                file_icon.innerHTML = `<svg width="64" height="64" viewBox="0 0 24 24" fill="none">
                <path d="M7 18H17V16H7V18Z" fill="currentColor" />
                <path d="M17 14H7V12H17V14Z" fill="currentColor" />
                <path d="M7 10H11V8H7V10Z" fill="currentColor" />
                <path fill-rule="evenodd" clip-rule="evenodd" d="M6 2C4.34315 2 3 3.34315 3 5V19C3 20.6569 4.34315 22 6 22H18C19.6569 22 21 20.6569 21 19V9C21 5.13401 17.866 2 14 2H6ZM6 4H13V9H19V19C19 19.5523 18.5523 20 18 20H6C5.44772 20 5 19.5523 5 19V5C5 4.44772 5.44772 4 6 4ZM15 4.10002C16.6113 4.4271 17.9413 5.52906 18.584 7H15V4.10002Z" fill="currentColor"/></svg>`;
                file_name = document.createElement('span');
                file_name.className = 'h6';
                file_name.innerText = files[index];
                file.appendChild(file_icon);
                file.appendChild(file_name);
                files_window.appendChild(file);
            }
        }
    }
    xhr.send('');
}

// Upload user file to server
function uploadFile(file) {
    file = file[0];
    var xhr = new XMLHttpRequest();
    var formData = new FormData();
    formData.append("user_file", file);
    xhr.open('POST', './upload_file');
    xhr.onreadystatechange = function() {
        if ( 4 == this.readyState ) {
            getUserFiles();
        }
    };
    xhr.send(formData);
}

// Open user file
function openFile(element) {
    if (element.getAttribute('selected') == 'true') {
        file_name = element.getAttribute('file-name');
        var xhr = new XMLHttpRequest();
        xhr.open('POST', './open_file');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200){
                location.reload();
            }
        }
        xhr.send('file_name=' + file_name);
    }
    files = document.querySelectorAll('.file');
    for (let index = 0; index < files.length; index++) {
        files[index].style.backgroundColor = 'transparent';
        files[index].setAttribute('selected', false);
    }
    element.style.backgroundColor = '#0d6efd';
    element.setAttribute('selected', true);
}

// Delete user file
function deleteFile() {
    files = document.querySelectorAll('.file');
    for (let index = 0; index < files.length; index++) {
        if (files[index].getAttribute('selected') == 'true') {
            file_name = files[index].getAttribute('file-name');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', './delete_file');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200){
                    getUserFiles();
                }
            }
            xhr.send('file_name=' + file_name);
        }
    }
}

// Save user file
function saveFile(file_name) {
    if (file_name != ':') {
        file_name = prompt('Введите имя файла.');
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './save_file');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('fileName=' + file_name);
}
