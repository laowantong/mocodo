function switchOnFlashlight(event) {
    document.documentElement.classList.toggle('flashlight');
    document.addEventListener('mousemove', trackMouse);
    document.addEventListener('mousedown', switchOffFlashlight);
    trackMouse(event);
}

function switchOffFlashlight() {
    document.documentElement.classList.toggle('flashlight');
    document.removeEventListener('mousemove', trackMouse);
    document.removeEventListener('mousedown', switchOffFlashlight);
    document.getElementById('flashlight').checked = false;
}

function trackMouse(event) {
    document.documentElement.style.setProperty('--cursorXPos', event.clientX + 'px');
    document.documentElement.style.setProperty('--cursorYPos', event.clientY + 'px');
}
