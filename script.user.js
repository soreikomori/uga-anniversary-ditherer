// ==UserScript==
// @name         UGA's 3rd Anniversary BMO
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  Print Images with 64 Colors!!!!!!
// @author       soreikomori
// @match        https://pixelplace.io/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=pixelplace.io
// @run-at       document-start
// @grant        none
// ==/UserScript==

// Original by Bambi1!

let chatting = false;
let pixelArray = [];
let delayBetweenPixels = 25;

function fix(a, b) {
    Object.defineProperty(window.console, a, {configurable:false,enumerable:true,writable:false,value:b});
}
fix('log', console.log);
fix('warn', console.warn);
fix('error', console.error);
fix('info', console.info);

const originalWebSocket = window.WebSocket;
var socket;

class WebSocketHook extends originalWebSocket {
    constructor(a, b) {
        super(a, b);
        socket = this;
    }
}
window.WebSocket = WebSocketHook;

function placePix(x, y, col) {
    socket.send(`42["p",[${x},${y},${col},1]]`);
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'j' && !chatting) {
        var coordinatesElement = document.getElementById('coordinates');
        if (coordinatesElement) {
            var coordinatesValue = coordinatesElement.textContent;
            var [x, y] = coordinatesValue.split(',').map(Number);
            console.log(x, y);
            image(x, y);
        }
    }
});

function image(SX, SY) {
    if (pixelArray.length === 0) {
        console.warn("No pixel array provided!");
        return;
    }
    let rowIndex = 0;

    function placeNextRow() {
        if (rowIndex < pixelArray.length) {
            const row = pixelArray[rowIndex];
            let columnIndex = 0;

            function placeNextPixel() {
                if (columnIndex < row.length) {
                    const col = row[columnIndex];
                    if (col >= 0 && col <= 63) {
                        placePix(SX + columnIndex, SY + rowIndex, col);
                    }
                    columnIndex++;
                    setTimeout(placeNextPixel, delayBetweenPixels);
                } else {
                    rowIndex++;
                    placeNextRow();
                }
            }
            placeNextPixel();
        }
    }
    placeNextRow();
}

document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.querySelector('input[name="chat"]');
    if (chatInput) {
        chatInput.addEventListener('focus', () => chatting = true);
        chatInput.addEventListener('blur', () => chatting = false);
    }

    function createDraggableWindow(title, content) {
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.top = '15%';
        container.style.left = '15%';
        container.style.background = 'rgba(0,0,0,0.8)';
        container.style.color = 'white';
        container.style.padding = '10px';
        container.style.borderRadius = '5px';
        container.style.zIndex = '10000';
        container.style.cursor = 'move';
        container.style.width = '320px';
        container.innerHTML = `<strong>${title}</strong>`;
        container.appendChild(content);
        document.body.appendChild(container);

        let offsetX, offsetY, isDragging = false;
        container.addEventListener('mousedown', function(e) {
            isDragging = true;
            offsetX = e.clientX - container.getBoundingClientRect().left;
            offsetY = e.clientY - container.getBoundingClientRect().top;
        });
        document.addEventListener('mousemove', function(e) {
            if (isDragging) {
                container.style.left = `${e.clientX - offsetX}px`;
                container.style.top = `${e.clientY - offsetY}px`;
            }
        });
        document.addEventListener('mouseup', function() {
            isDragging = false;
        });
        return container;
    }

    const inputField = document.createElement('textarea');
    inputField.placeholder = "Paste pixel array here...";
    inputField.style.width = '100%';
    inputField.style.height = '100px';

    const applyButton = document.createElement('button');
    applyButton.innerText = "Apply";
    applyButton.style.marginTop = '5px';
    applyButton.onclick = function() {
        try {
            pixelArray = JSON.parse(inputField.value);
            console.log("Pixel array updated.");
        } catch (e) {
            console.error("Invalid array format!");
        }
    };

    const inputContainer = document.createElement('div');
    inputContainer.appendChild(inputField);
    inputContainer.appendChild(applyButton);
    createDraggableWindow("Pixel Array Input", inputContainer);

    const delaySlider = document.createElement('input');
    delaySlider.type = 'range';
    delaySlider.min = '10';
    delaySlider.max = '200';
    delaySlider.value = delayBetweenPixels;
    delaySlider.style.width = '100%';

    const delayLabel = document.createElement('span');
    delayLabel.innerText = `Delay: ${delaySlider.value}ms`;

    delaySlider.oninput = function() {
        delayBetweenPixels = parseInt(this.value);
        delayLabel.innerText = `Delay: ${this.value}ms`;
    };

    const delayContainer = document.createElement('div');
    delayContainer.appendChild(delayLabel);
    delayContainer.appendChild(delaySlider);
    createDraggableWindow("Pixel Placement Speed", delayContainer);
});