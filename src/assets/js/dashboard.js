"use strict";

let notifyModal = (message) => {
    let modalBox = document.querySelector("#modalContainer");
    let messageDic = modalBox.querySelector("#message");
    let messageContentDiv = messageDic.querySelector(".message-content");

    messageContentDiv.innerText = message;

    messageDic.classList.remove('hidden');
    modalBox.classList.remove('hidden');
};

let hideMessage = (e) => {
    let modalBox = document.querySelector("#modalContainer");
    let messageDic = modalBox.querySelector("#message");

    messageDic.classList.add('hidden');
    modalBox.classList.add('hidden');

    e.stopPropagation();
};

let showCaForm = () => {
    let caForm = document.querySelector("#caForm");
    let modalBox = document.querySelector("#modalContainer");

    modalBox.classList.remove('hidden');
    caForm.classList.remove('hidden');


};

let hideCaForm = (e) => {
    let caForm = document.querySelector("#caForm");
    let modalBox = document.querySelector("#modalContainer");

    caForm.reset();
    modalBox.classList.add('hidden');
    caForm.classList.add('hidden');
};


let handleCaFormSubmit = (e) => {
    let caForm = document.querySelector("#caForm");

    // send the requests to create the form
    e.preventDefault();
    let appName = caForm.querySelector("#name");
    let appDescription = caForm.querySelector("#description");

    fetch("/api/app", {
        method: "post",
        body: JSON.stringify({name: appName.value, description: appDescription.value}),
        credentials: "include",
        headers: {
            "content-type": "application/json; charset=utf-8"
        }
    }).then((res) => {
        // reset the form
        if(res.status.toString().charAt(0) != '2'){
            // handle the error
            let errorPar = caForm.querySelector('#nameExistError');
            errorPar.classList.remove('hidden');

        } else {

            caForm.reset();
            hideCaForm();

            let message = "The application will be validated by an admin before any use";
            notifyModal(message);
            // messageDic.classList.remove("hidden");
        }

    }).catch((err) => {
        console.log(err.message);
        hideCaForm();
        notifyModal("An error occured, please try later")
    })

    // e.preventDefault();
};

document.addEventListener('DOMContentLoaded', () => {

    let addAppLink = document.querySelector("#addApp");
    let caFormCloseBtn = document.querySelector("#caFormCloseBtn");
    let modalBox = document.querySelector("#modalContainer");
    let caForm = document.querySelector("#caForm");

    let messageDiv = modalBox.querySelector("#message");

    // handle the click of the add app form
    addAppLink.addEventListener('click', (e) => {
        showCaForm();
    });

    // handle the form submit
    caForm.addEventListener('submit', handleCaFormSubmit);


    let messageDivCloseBtn = messageDiv.querySelector(".close");
    messageDivCloseBtn.addEventListener('click', hideMessage);

    //
    caForm.addEventListener('click', (e) => e.stopPropagation());
    messageDiv.addEventListener('click', (e) => e.stopPropagation());


    // handle the click on the close button of the form
    caFormCloseBtn.addEventListener('click', hideCaForm);

    // hide the modal
    modalBox.addEventListener('click', (e) => modalBox.classList.add('hidden'));

    let appName = caForm.querySelector("#name");
    let errorPar = caForm.querySelector('#nameExistError');

    appName.addEventListener('keyup', () => {
        if(!errorPar.classList.contains('hidden')){
            errorPar.classList.add('hidden')
        }

        // check if the app exist for the user

        fetch('/api/app?name='+appName.value, {
            method: 'get',
            credentials: "include",
            headers: {
                "content-type": "application/json; charset=utf-8"
            }
        }).then((res)=>{
            let errorPar = caForm.querySelector('#nameExistError');
            let caFormSubmitBtn = caForm.querySelector('caFormSubmitBtn')
            // if res.status is 200 then show the error else hide the error
            if(res.status === 200){
                errorPar.classList.remove('hidden');
                caFormSubmitBtn.disabled = true;
            } else if(res.status !== 200 && !errorPar.classList.contains('hidden')) {
                errorPar.classList.add('hidden');
                caFormSubmitBtn.disabled = false;
            }
            console.log(1222)
        }).catch(err => {
            // do nothing
        })
    })
});
