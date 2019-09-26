(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["js/dashboard"],{

/***/ "./assets/js/dashboard.js":
/*!********************************!*\
  !*** ./assets/js/dashboard.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _require = __webpack_require__(/*! ./dashboard/addAppForm */ "./assets/js/dashboard/addAppForm.js"),
    caFormJsStarter = _require.caFormJsStarter;

var handleAppReload = function handleAppReload() {};

document.addEventListener('DOMContentLoaded', function () {
  caFormJsStarter();
});

/***/ }),

/***/ "./assets/js/dashboard/addAppForm.js":
/*!*******************************************!*\
  !*** ./assets/js/dashboard/addAppForm.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _this = this;

var _require = __webpack_require__(/*! ./../notifyModal */ "./assets/js/notifyModal.js"),
    notifyModal = _require.notifyModal,
    hideMessage = _require.hideMessage;

module.exports.showCaForm = function () {
  var caForm = document.querySelector("#caForm");
  var modalBox = document.querySelector("#modalContainer");
  modalBox.classList.remove('hidden');
  caForm.classList.remove('hidden');
};

module.exports.hideCaForm = function (e) {
  var caForm = document.querySelector("#caForm");
  var modalBox = document.querySelector("#modalContainer");
  caForm.reset();
  modalBox.classList.add('hidden');
  caForm.classList.add('hidden');
};

module.exports.handleCaFormSubmit = function (e) {
  var caForm = document.querySelector("#caForm"); // send the requests to create the form

  e.preventDefault();
  var appName = caForm.querySelector("#name");
  var appDescription = caForm.querySelector("#description");
  fetch("/api/app", {
    method: "post",
    body: JSON.stringify({
      name: appName.value,
      description: appDescription.value
    }),
    credentials: "include",
    headers: {
      "content-type": "application/json; charset=utf-8"
    }
  }).then(function (res) {
    // reset the form
    if (res.status.toString().charAt(0) !== '2') {
      // handle the error
      var errorPar = caForm.querySelector('#nameExistError');
      errorPar.classList.remove('hidden');
    } else {
      caForm.reset();

      _this.hideCaForm();

      var message = "The application will be validated by an admin before any use";
      notifyModal(message); // messageDic.classList.remove("hidden");
    }
  })["catch"](function (err) {
    console.log(err.message);

    _this.hideCaForm();

    notifyModal("An error occured, please try later");
  }); // e.preventDefault();
};

module.exports.checkNameExist = function () {
  var caForm = document.querySelector("#caForm");
  var appName = caForm.querySelector("#name");
  var errorPar = caForm.querySelector('#nameExistError');

  if (!errorPar.classList.contains('hidden')) {
    errorPar.classList.add('hidden');
  } // check if the app exist for the user


  fetch('/api/app?name=' + appName.value, {
    method: 'get',
    credentials: "include",
    headers: {
      "content-type": "application/json; charset=utf-8"
    }
  }).then(function (res) {
    var errorPar = caForm.querySelector('#nameExistError');
    var caFormSubmitBtn = caForm.querySelector('caFormSubmitBtn'); // if res.status is 200 then show the error else hide the error

    if (res.status === 200) {
      errorPar.classList.remove('hidden');
      caFormSubmitBtn.disabled = true;
    } else if (res.status !== 200 && !errorPar.classList.contains('hidden')) {
      errorPar.classList.add('hidden');
      caFormSubmitBtn.disabled = false;
    } // console.log(1222)

  })["catch"](function (err) {// do nothing
  });
};

module.exports.caFormJsStarter = function () {
  var addAppLink = document.querySelector("#addApp");
  var caFormCloseBtn = document.querySelector("#caFormCloseBtn");
  var modalBox = document.querySelector("#modalContainer");
  var caForm = document.querySelector("#caForm");
  var messageDiv = modalBox.querySelector("#message"); // handle the click of the add app form

  addAppLink.addEventListener('click', function (e) {
    _this.showCaForm();
  }); // handle the form submit

  caForm.addEventListener('submit', _this.handleCaFormSubmit);
  var messageDivCloseBtn = messageDiv.querySelector(".close");
  messageDivCloseBtn.addEventListener('click', _this.hideMessage); // stop propagation of the click event

  caForm.addEventListener('click', function (e) {
    return e.stopPropagation();
  });
  messageDiv.addEventListener('click', function (e) {
    return e.stopPropagation();
  }); // handle the click on the close button of the form

  caFormCloseBtn.addEventListener('click', _this.hideCaForm); // hide the modal

  modalBox.addEventListener('click', function (e) {
    return modalBox.classList.add('hidden');
  });
  var appName = caForm.querySelector("#name");
  appName.addEventListener('keyup', _this.checkNameExist);
};

/***/ }),

/***/ "./assets/js/notifyModal.js":
/*!**********************************!*\
  !*** ./assets/js/notifyModal.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports.notifyModal = function (message) {
  var modalBox = document.querySelector("#modalContainer");
  var messageDic = modalBox.querySelector("#message");
  var messageContentDiv = messageDic.querySelector(".message-content");
  messageContentDiv.innerText = message;
  messageDic.classList.remove('hidden');
  modalBox.classList.remove('hidden');
};

module.exports.hideMessage = function (e) {
  var modalBox = document.querySelector("#modalContainer");
  var messageDic = modalBox.querySelector("#message");
  messageDic.classList.add('hidden');
  modalBox.classList.add('hidden');
  e.stopPropagation();
};

/***/ })

},[["./assets/js/dashboard.js","runtime"]]]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9hc3NldHMvanMvZGFzaGJvYXJkLmpzIiwid2VicGFjazovLy8uL2Fzc2V0cy9qcy9kYXNoYm9hcmQvYWRkQXBwRm9ybS5qcyIsIndlYnBhY2s6Ly8vLi9hc3NldHMvanMvbm90aWZ5TW9kYWwuanMiXSwibmFtZXMiOlsicmVxdWlyZSIsImNhRm9ybUpzU3RhcnRlciIsImhhbmRsZUFwcFJlbG9hZCIsImRvY3VtZW50IiwiYWRkRXZlbnRMaXN0ZW5lciIsIm5vdGlmeU1vZGFsIiwiaGlkZU1lc3NhZ2UiLCJtb2R1bGUiLCJleHBvcnRzIiwic2hvd0NhRm9ybSIsImNhRm9ybSIsInF1ZXJ5U2VsZWN0b3IiLCJtb2RhbEJveCIsImNsYXNzTGlzdCIsInJlbW92ZSIsImhpZGVDYUZvcm0iLCJlIiwicmVzZXQiLCJhZGQiLCJoYW5kbGVDYUZvcm1TdWJtaXQiLCJwcmV2ZW50RGVmYXVsdCIsImFwcE5hbWUiLCJhcHBEZXNjcmlwdGlvbiIsImZldGNoIiwibWV0aG9kIiwiYm9keSIsIkpTT04iLCJzdHJpbmdpZnkiLCJuYW1lIiwidmFsdWUiLCJkZXNjcmlwdGlvbiIsImNyZWRlbnRpYWxzIiwiaGVhZGVycyIsInRoZW4iLCJyZXMiLCJzdGF0dXMiLCJ0b1N0cmluZyIsImNoYXJBdCIsImVycm9yUGFyIiwibWVzc2FnZSIsImVyciIsImNvbnNvbGUiLCJsb2ciLCJjaGVja05hbWVFeGlzdCIsImNvbnRhaW5zIiwiY2FGb3JtU3VibWl0QnRuIiwiZGlzYWJsZWQiLCJhZGRBcHBMaW5rIiwiY2FGb3JtQ2xvc2VCdG4iLCJtZXNzYWdlRGl2IiwibWVzc2FnZURpdkNsb3NlQnRuIiwic3RvcFByb3BhZ2F0aW9uIiwibWVzc2FnZURpYyIsIm1lc3NhZ2VDb250ZW50RGl2IiwiaW5uZXJUZXh0Il0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQWE7O2VBRWFBLG1CQUFPLENBQUMsbUVBQUQsQztJQUExQkMsZSxZQUFBQSxlOztBQUVQLElBQUlDLGVB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VCxDQUF1QixpQkFBdkIsQ0FBZjtBQUNBLE1BQUl5QyxVQUFVLEdBQUd4QyxRQUFRLENBQUNELGFBQVQsQ0FBdUIsVUFBdkIsQ0FBakI7QUFFQXlDLFlBQVUsQ0FBQ3ZDLFNBQVgsQ0FBcUJLLEdBQXJCLENBQXlCLFFBQXpCO0FBQ0FOLFVBQVEsQ0FBQ0MsU0FBVCxDQUFtQkssR0FBbkIsQ0FBdUIsUUFBdkI7QUFFQUYsR0FBQyxDQUFDbUMsZUFBRjtBQUNILENBUkQsQyIsImZpbGUiOiJqcy9kYXNoYm9hcmQuanMiLCJzb3VyY2VzQ29udGVudCI6WyJcInVzZSBzdHJpY3RcIjtcblxuY29uc3Qge2NhRm9ybUpzU3RhcnRlcn0gPSByZXF1aXJlKCcuL2Rhc2hib2FyZC9hZGRBcHBGb3JtJylcblxubGV0IGhhbmRsZUFwcFJlbG9hZCA9ICgpID0+IHtcblxufTtcblxuZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHtcbiAgICBjYUZvcm1Kc1N0YXJ0ZXIoKTtcbn0pO1xuIiwiXCJ1c2Ugc3RyaWN0XCI7XG5sZXQge25vdGlmeU1vZGFsLCBoaWRlTWVzc2FnZX0gPSByZXF1aXJlKCcuLy4uL25vdGlmeU1vZGFsJyk7XG5cbm1vZHVsZS5leHBvcnRzLnNob3dDYUZvcm0gPSAoKSA9PiB7XG4gICAgbGV0IGNhRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjY2FGb3JtXCIpO1xuICAgIGxldCBtb2RhbEJveCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjbW9kYWxDb250YWluZXJcIik7XG5cbiAgICBtb2RhbEJveC5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICBjYUZvcm0uY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG5cblxufTtcblxubW9kdWxlLmV4cG9ydHMuaGlkZUNhRm9ybSA9IChlKSA9PiB7XG4gICAgbGV0IGNhRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjY2FGb3JtXCIpO1xuICAgIGxldCBtb2RhbEJveCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjbW9kYWxDb250YWluZXJcIik7XG5cbiAgICBjYUZvcm0ucmVzZXQoKTtcbiAgICBtb2RhbEJveC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICBjYUZvcm0uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59O1xuXG5cbm1vZHVsZS5leHBvcnRzLmhhbmRsZUNhRm9ybVN1Ym1pdCA9IChlKSA9PiB7XG4gICAgbGV0IGNhRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjY2FGb3JtXCIpO1xuXG4gICAgLy8gc2VuZCB0aGUgcmVxdWVzdHMgdG8gY3JlYXRlIHRoZSBmb3JtXG4gICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xuICAgIGxldCBhcHBOYW1lID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoXCIjbmFtZVwiKTtcbiAgICBsZXQgYXBwRGVzY3JpcHRpb24gPSBjYUZvcm0ucXVlcnlTZWxlY3RvcihcIiNkZXNjcmlwdGlvblwiKTtcblxuICAgIGZldGNoKFwiL2FwaS9hcHBcIiwge1xuICAgICAgICBtZXRob2Q6IFwicG9zdFwiLFxuICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeSh7bmFtZTogYXBwTmFtZS52YWx1ZSwgZGVzY3JpcHRpb246IGFwcERlc2NyaXB0aW9uLnZhbHVlfSksXG4gICAgICAgIGNyZWRlbnRpYWxzOiBcImluY2x1ZGVcIixcbiAgICAgICAgaGVhZGVyczoge1xuICAgICAgICAgICAgXCJjb250ZW50LXR5cGVcIjogXCJhcHBsaWNhdGlvbi9qc29uOyBjaGFyc2V0PXV0Zi04XCJcbiAgICAgICAgfVxuICAgIH0pLnRoZW4oKHJlcykgPT4ge1xuICAgICAgICAvLyByZXNldCB0aGUgZm9ybVxuICAgICAgICBpZihyZXMuc3RhdHVzLnRvU3RyaW5nKCkuY2hhckF0KDApICE9PSAnMicpe1xuICAgICAgICAgICAgLy8gaGFuZGxlIHRoZSBlcnJvclxuICAgICAgICAgICAgbGV0IGVycm9yUGFyID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoJyNuYW1lRXhpc3RFcnJvcicpO1xuICAgICAgICAgICAgZXJyb3JQYXIuY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG5cbiAgICAgICAgfSBlbHNlIHtcblxuICAgICAgICAgICAgY2FGb3JtLnJlc2V0KCk7XG4gICAgICAgICAgICB0aGlzLmhpZGVDYUZvcm0oKTtcblxuICAgICAgICAgICAgbGV0IG1lc3NhZ2UgPSBcIlRoZSBhcHBsaWNhdGlvbiB3aWxsIGJlIHZhbGlkYXRlZCBieSBhbiBhZG1pbiBiZWZvcmUgYW55IHVzZVwiO1xuICAgICAgICAgICAgbm90aWZ5TW9kYWwobWVzc2FnZSk7XG4gICAgICAgICAgICAvLyBtZXNzYWdlRGljLmNsYXNzTGlzdC5yZW1vdmUoXCJoaWRkZW5cIik7XG4gICAgICAgIH1cblxuICAgIH0pLmNhdGNoKChlcnIpID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coZXJyLm1lc3NhZ2UpO1xuICAgICAgICB0aGlzLmhpZGVDYUZvcm0oKTtcbiAgICAgICAgbm90aWZ5TW9kYWwoXCJBbiBlcnJvciBvY2N1cmVkLCBwbGVhc2UgdHJ5IGxhdGVyXCIpXG4gICAgfSlcblxuICAgIC8vIGUucHJldmVudERlZmF1bHQoKTtcbn07XG5cblxubW9kdWxlLmV4cG9ydHMuY2hlY2tOYW1lRXhpc3QgPSAoKSA9PiB7XG4gICAgbGV0IGNhRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjY2FGb3JtXCIpO1xuXG4gICAgbGV0IGFwcE5hbWUgPSBjYUZvcm0ucXVlcnlTZWxlY3RvcihcIiNuYW1lXCIpO1xuICAgIGxldCBlcnJvclBhciA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKCcjbmFtZUV4aXN0RXJyb3InKTtcblxuICAgIGlmKCFlcnJvclBhci5jbGFzc0xpc3QuY29udGFpbnMoJ2hpZGRlbicpKXtcbiAgICAgICAgZXJyb3JQYXIuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJylcbiAgICB9XG5cbiAgICAvLyBjaGVjayBpZiB0aGUgYXBwIGV4aXN0IGZvciB0aGUgdXNlclxuXG4gICAgZmV0Y2goJy9hcGkvYXBwP25hbWU9JythcHBOYW1lLnZhbHVlLCB7XG4gICAgICAgIG1ldGhvZDogJ2dldCcsXG4gICAgICAgIGNyZWRlbnRpYWxzOiBcImluY2x1ZGVcIixcbiAgICAgICAgaGVhZGVyczoge1xuICAgICAgICAgICAgXCJjb250ZW50LXR5cGVcIjogXCJhcHBsaWNhdGlvbi9qc29uOyBjaGFyc2V0PXV0Zi04XCJcbiAgICAgICAgfVxuICAgIH0pLnRoZW4oKHJlcyk9PntcbiAgICAgICAgbGV0IGVycm9yUGFyID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoJyNuYW1lRXhpc3RFcnJvcicpO1xuICAgICAgICBsZXQgY2FGb3JtU3VibWl0QnRuID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoJ2NhRm9ybVN1Ym1pdEJ0bicpXG5cbiAgICAgICAgLy8gaWYgcmVzLnN0YXR1cyBpcyAyMDAgdGhlbiBzaG93IHRoZSBlcnJvciBlbHNlIGhpZGUgdGhlIGVycm9yXG4gICAgICAgIGlmKHJlcy5zdGF0dXMgPT09IDIwMCl7XG4gICAgICAgICAgICBlcnJvclBhci5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICAgICAgICAgIGNhRm9ybVN1Ym1pdEJ0bi5kaXNhYmxlZCA9IHRydWU7XG4gICAgICAgIH0gZWxzZSBpZihyZXMuc3RhdHVzICE9PSAyMDAgJiYgIWVycm9yUGFyLmNsYXNzTGlzdC5jb250YWlucygnaGlkZGVuJykpIHtcbiAgICAgICAgICAgIGVycm9yUGFyLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgICAgICAgY2FGb3JtU3VibWl0QnRuLmRpc2FibGVkID0gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgLy8gY29uc29sZS5sb2coMTIyMilcbiAgICB9KS5jYXRjaChlcnIgPT4ge1xuICAgICAgICAvLyBkbyBub3RoaW5nXG4gICAgfSk7XG59O1xuXG5tb2R1bGUuZXhwb3J0cy5jYUZvcm1Kc1N0YXJ0ZXIgPSAoKSA9PiB7XG5cbiAgICBsZXQgYWRkQXBwTGluayA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjYWRkQXBwXCIpO1xuICAgIGxldCBjYUZvcm1DbG9zZUJ0biA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjY2FGb3JtQ2xvc2VCdG5cIik7XG4gICAgbGV0IG1vZGFsQm94ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNtb2RhbENvbnRhaW5lclwiKTtcbiAgICBsZXQgY2FGb3JtID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNjYUZvcm1cIik7XG5cbiAgICBsZXQgbWVzc2FnZURpdiA9IG1vZGFsQm94LnF1ZXJ5U2VsZWN0b3IoXCIjbWVzc2FnZVwiKTtcblxuICAgIC8vIGhhbmRsZSB0aGUgY2xpY2sgb2YgdGhlIGFkZCBhcHAgZm9ybVxuICAgIGFkZEFwcExpbmsuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoZSkgPT4ge1xuICAgICAgICB0aGlzLnNob3dDYUZvcm0oKTtcbiAgICB9KTtcblxuICAgIC8vIGhhbmRsZSB0aGUgZm9ybSBzdWJtaXRcbiAgICBjYUZvcm0uYWRkRXZlbnRMaXN0ZW5lcignc3VibWl0JywgdGhpcy5oYW5kbGVDYUZvcm1TdWJtaXQpO1xuXG5cbiAgICBsZXQgbWVzc2FnZURpdkNsb3NlQnRuID0gbWVzc2FnZURpdi5xdWVyeVNlbGVjdG9yKFwiLmNsb3NlXCIpO1xuICAgIG1lc3NhZ2VEaXZDbG9zZUJ0bi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIHRoaXMuaGlkZU1lc3NhZ2UpO1xuXG4gICAgLy8gc3RvcCBwcm9wYWdhdGlvbiBvZiB0aGUgY2xpY2sgZXZlbnRcbiAgICBjYUZvcm0uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoZSkgPT4gZS5zdG9wUHJvcGFnYXRpb24oKSk7XG4gICAgbWVzc2FnZURpdi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiBlLnN0b3BQcm9wYWdhdGlvbigpKTtcblxuXG4gICAgLy8gaGFuZGxlIHRoZSBjbGljayBvbiB0aGUgY2xvc2UgYnV0dG9uIG9mIHRoZSBmb3JtXG4gICAgY2FGb3JtQ2xvc2VCdG4uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCB0aGlzLmhpZGVDYUZvcm0pO1xuXG4gICAgLy8gaGlkZSB0aGUgbW9kYWxcbiAgICBtb2RhbEJveC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiBtb2RhbEJveC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKSk7XG5cbiAgICBsZXQgYXBwTmFtZSA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKFwiI25hbWVcIik7XG5cbiAgICBhcHBOYW1lLmFkZEV2ZW50TGlzdGVuZXIoJ2tleXVwJywgdGhpcy5jaGVja05hbWVFeGlzdCk7XG59O1xuIiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbm1vZHVsZS5leHBvcnRzLm5vdGlmeU1vZGFsID0gKG1lc3NhZ2UpID0+IHtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuICAgIGxldCBtZXNzYWdlRGljID0gbW9kYWxCb3gucXVlcnlTZWxlY3RvcihcIiNtZXNzYWdlXCIpO1xuICAgIGxldCBtZXNzYWdlQ29udGVudERpdiA9IG1lc3NhZ2VEaWMucXVlcnlTZWxlY3RvcihcIi5tZXNzYWdlLWNvbnRlbnRcIik7XG5cbiAgICBtZXNzYWdlQ29udGVudERpdi5pbm5lclRleHQgPSBtZXNzYWdlO1xuXG4gICAgbWVzc2FnZURpYy5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICBtb2RhbEJveC5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbn07XG5cbm1vZHVsZS5leHBvcnRzLmhpZGVNZXNzYWdlID0gKGUpID0+IHtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuICAgIGxldCBtZXNzYWdlRGljID0gbW9kYWxCb3gucXVlcnlTZWxlY3RvcihcIiNtZXNzYWdlXCIpO1xuXG4gICAgbWVzc2FnZURpYy5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICBtb2RhbEJveC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcblxuICAgIGUuc3RvcFByb3BhZ2F0aW9uKCk7XG59O1xuIl0sInNvdXJjZVJvb3QiOiIifQ==