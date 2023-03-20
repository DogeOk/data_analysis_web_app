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
function createContextMenu(elements, functions) {
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

// Upload user files in web
function get_user_files() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', './user_files');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200){
            files = xhr.responseText;
            for (let file = 0; file < files.length; file++) {

            }
        }
    }
    xhr.send('login=' + login + '&password=' + password);
}
