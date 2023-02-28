document.addEventListener('click', function() {
    console.log('click');
    context_menu = document.getElementById('context-menu');
    context_menu.style.display = 'none';
}, false);

document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
}, false);
