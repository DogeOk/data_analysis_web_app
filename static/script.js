//Hide context menu on left click
document.addEventListener('click', function() {
    context_menu = document.getElementById('context-menu');
    context_menu.style.display = 'none';
}, false);

//Hide default context menu on right click
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
}, false);

//Create context menu with elements and actions
function create_context_menu(elements, functions) {
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

//Hide one element and show another element
function hideShow(hideBlock, showBlock) {
    document.getElementById(hideBlock).style.display = 'none';
    document.getElementById(showBlock).style.display = 'block';
}
