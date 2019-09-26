"use strict";

module.exports.notifyModal = (message) => {
    let modalBox = document.querySelector("#modalContainer");
    let messageDic = modalBox.querySelector("#message");
    let messageContentDiv = messageDic.querySelector(".message-content");

    messageContentDiv.innerText = message;

    messageDic.classList.remove('hidden');
    modalBox.classList.remove('hidden');
};

module.exports.hideMessage = (e) => {
    let modalBox = document.querySelector("#modalContainer");
    let messageDic = modalBox.querySelector("#message");

    messageDic.classList.add('hidden');
    modalBox.classList.add('hidden');

    e.stopPropagation();
};
