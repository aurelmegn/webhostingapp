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
  var appType = caForm.querySelector("#type");
  var csrfTokenField = caForm.querySelector("#csrf_token");
  fetch("/api/app", {
    method: "post",
    body: JSON.stringify({
      name: appName.value,
      description: appDescription.value,
      type: appType.value,
      csrf_token: csrfTokenField.value
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9hc3NldHMvanMvZGFzaGJvYXJkLmpzIiwid2VicGFjazovLy8uL2Fzc2V0cy9qcy9kYXNoYm9hcmQvYWRkQXBwRm9ybS5qcyIsIndlYnBhY2s6Ly8vLi9hc3NldHMvanMvbm90aWZ5TW9kYWwuanMiXSwibmFtZXMiOlsicmVxdWlyZSIsImNhRm9ybUpzU3RhcnRlciIsImhhbmRsZUFwcFJlbG9hZCIsImRvY3VtZW50IiwiYWRkRXZlbnRMaXN0ZW5lciIsIm5vdGlmeU1vZGFsIiwiaGlkZU1lc3NhZ2UiLCJtb2R1bGUiLCJleHBvcnRzIiwic2hvd0NhRm9ybSIsImNhRm9ybSIsInF1ZXJ5U2VsZWN0b3IiLCJtb2RhbEJveCIsImNsYXNzTGlzdCIsInJlbW92ZSIsImhpZGVDYUZvcm0iLCJlIiwicmVzZXQiLCJhZGQiLCJoYW5kbGVDYUZvcm1TdWJtaXQiLCJwcmV2ZW50RGVmYXVsdCIsImFwcE5hbWUiLCJhcHBEZXNjcmlwdGlvbiIsImFwcFR5cGUiLCJjc3JmVG9rZW5GaWVsZCIsImZldGNoIiwibWV0aG9kIiwiYm9keSIsIkpTT04iLCJzdHJpbmdpZnkiLCJuYW1lIiwidmFsdWUiLCJkZXNjcmlwdGlvbiIsInR5cGUiLCJjc3JmX3Rva2VuIiwiY3JlZGVudGlhbHMiLCJoZWFkZXJzIiwidGhlbiIsInJlcyIsInN0YXR1cyIsInRvU3RyaW5nIiwiY2hhckF0IiwiZXJyb3JQYXIiLCJtZXNzYWdlIiwiZXJyIiwiY29uc29sZSIsImxvZyIsImNoZWNrTmFtZUV4aXN0IiwiY29udGFpbnMiLCJjYUZvcm1TdWJtaXRCdG4iLCJkaXNhYmxlZCIsImFkZEFwcExpbmsiLCJjYUZvcm1DbG9zZUJ0biIsIm1lc3NhZ2VEaXYiLCJtZXNzYWdlRGl2Q2xvc2VCdG4iLCJzdG9wUHJvcGFnYXRpb24iLCJtZXNzYWdlRGljIiwibWVzc2FnZUNvbnRlbnREaXYiLCJpbm5lclRleHQiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7QUFBYTs7ZUFFYUEsbUJB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QkFBaUIsQ0FBQ0MsU0FBbEIsR0FBOEJmLE9BQTlCO0FBRUFhLFlBQVUsQ0FBQzNDLFNBQVgsQ0FBcUJDLE1BQXJCLENBQTRCLFFBQTVCO0FBQ0FGLFVBQVEsQ0FBQ0MsU0FBVCxDQUFtQkMsTUFBbkIsQ0FBMEIsUUFBMUI7QUFDSCxDQVREOztBQVdBUCxNQUFNLENBQUNDLE9BQVAsQ0FBZUYsV0FBZixHQUE2QixVQUFDVSxDQUFELEVBQU87QUFDaEMsTUFBSUosUUFBUSxHQUFHVCxRQUFRLENBQUNRLGFBQVQsQ0FBdUIsaUJBQXZCLENBQWY7QUFDQSxNQUFJNkMsVUFBVSxHQUFHNUMsUUFBUSxDQUFDRCxhQUFULENBQXVCLFVBQXZCLENBQWpCO0FBRUE2QyxZQUFVLENBQUMzQyxTQUFYLENBQXFCSyxHQUFyQixDQUF5QixRQUF6QjtBQUNBTixVQUFRLENBQUNDLFNBQVQsQ0FBbUJLLEdBQW5CLENBQXVCLFFBQXZCO0FBRUFGLEdBQUMsQ0FBQ3VDLGVBQUY7QUFDSCxDQVJELEMiLCJmaWxlIjoianMvZGFzaGJvYXJkLmpzIiwic291cmNlc0NvbnRlbnQiOlsiXCJ1c2Ugc3RyaWN0XCI7XG5cbmNvbnN0IHtjYUZvcm1Kc1N0YXJ0ZXJ9ID0gcmVxdWlyZSgnLi9kYXNoYm9hcmQvYWRkQXBwRm9ybScpXG5cbmxldCBoYW5kbGVBcHBSZWxvYWQgPSAoKSA9PiB7XG5cbn07XG5cbmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCAoKSA9PiB7XG4gICAgY2FGb3JtSnNTdGFydGVyKCk7XG59KTtcbiIsIlwidXNlIHN0cmljdFwiO1xubGV0IHtub3RpZnlNb2RhbCwgaGlkZU1lc3NhZ2V9ID0gcmVxdWlyZSgnLi8uLi9ub3RpZnlNb2RhbCcpO1xuXG5tb2R1bGUuZXhwb3J0cy5zaG93Q2FGb3JtID0gKCkgPT4ge1xuICAgIGxldCBjYUZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NhRm9ybVwiKTtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuXG4gICAgbW9kYWxCb3guY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG4gICAgY2FGb3JtLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuXG5cbn07XG5cbm1vZHVsZS5leHBvcnRzLmhpZGVDYUZvcm0gPSAoZSkgPT4ge1xuICAgIGxldCBjYUZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NhRm9ybVwiKTtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuXG4gICAgY2FGb3JtLnJlc2V0KCk7XG4gICAgbW9kYWxCb3guY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgY2FGb3JtLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xufTtcblxuXG5tb2R1bGUuZXhwb3J0cy5oYW5kbGVDYUZvcm1TdWJtaXQgPSAoZSkgPT4ge1xuICAgIGxldCBjYUZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NhRm9ybVwiKTtcblxuICAgIC8vIHNlbmQgdGhlIHJlcXVlc3RzIHRvIGNyZWF0ZSB0aGUgZm9ybVxuICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICBsZXQgYXBwTmFtZSA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKFwiI25hbWVcIik7XG4gICAgbGV0IGFwcERlc2NyaXB0aW9uID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoXCIjZGVzY3JpcHRpb25cIik7XG4gICAgbGV0IGFwcFR5cGUgPSBjYUZvcm0ucXVlcnlTZWxlY3RvcihcIiN0eXBlXCIpO1xuICAgIGxldCBjc3JmVG9rZW5GaWVsZCA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKFwiI2NzcmZfdG9rZW5cIik7XG5cbiAgICBmZXRjaChcIi9hcGkvYXBwXCIsIHtcbiAgICAgICAgbWV0aG9kOiBcInBvc3RcIixcbiAgICAgICAgYm9keTogSlNPTi5zdHJpbmdpZnkoe25hbWU6IGFwcE5hbWUudmFsdWUsIGRlc2NyaXB0aW9uOiBhcHBEZXNjcmlwdGlvbi52YWx1ZSwgdHlwZTogYXBwVHlwZS52YWx1ZSwgY3NyZl90b2tlbjogY3NyZlRva2VuRmllbGQudmFsdWV9KSxcbiAgICAgICAgY3JlZGVudGlhbHM6IFwiaW5jbHVkZVwiLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgICBcImNvbnRlbnQtdHlwZVwiOiBcImFwcGxpY2F0aW9uL2pzb247IGNoYXJzZXQ9dXRmLThcIlxuICAgICAgICB9XG4gICAgfSkudGhlbigocmVzKSA9PiB7XG4gICAgICAgIC8vIHJlc2V0IHRoZSBmb3JtXG4gICAgICAgIGlmKHJlcy5zdGF0dXMudG9TdHJpbmcoKS5jaGFyQXQoMCkgIT09ICcyJyl7XG4gICAgICAgICAgICAvLyBoYW5kbGUgdGhlIGVycm9yXG4gICAgICAgICAgICBsZXQgZXJyb3JQYXIgPSBjYUZvcm0ucXVlcnlTZWxlY3RvcignI25hbWVFeGlzdEVycm9yJyk7XG4gICAgICAgICAgICBlcnJvclBhci5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcblxuICAgICAgICB9IGVsc2Uge1xuXG4gICAgICAgICAgICBjYUZvcm0ucmVzZXQoKTtcbiAgICAgICAgICAgIHRoaXMuaGlkZUNhRm9ybSgpO1xuXG4gICAgICAgICAgICBsZXQgbWVzc2FnZSA9IFwiVGhlIGFwcGxpY2F0aW9uIHdpbGwgYmUgdmFsaWRhdGVkIGJ5IGFuIGFkbWluIGJlZm9yZSBhbnkgdXNlXCI7XG4gICAgICAgICAgICBub3RpZnlNb2RhbChtZXNzYWdlKTtcbiAgICAgICAgICAgIC8vIG1lc3NhZ2VEaWMuY2xhc3NMaXN0LnJlbW92ZShcImhpZGRlblwiKTtcbiAgICAgICAgfVxuXG4gICAgfSkuY2F0Y2goKGVycikgPT4ge1xuICAgICAgICBjb25zb2xlLmxvZyhlcnIubWVzc2FnZSk7XG4gICAgICAgIHRoaXMuaGlkZUNhRm9ybSgpO1xuICAgICAgICBub3RpZnlNb2RhbChcIkFuIGVycm9yIG9jY3VyZWQsIHBsZWFzZSB0cnkgbGF0ZXJcIilcbiAgICB9KVxuXG4gICAgLy8gZS5wcmV2ZW50RGVmYXVsdCgpO1xufTtcblxuXG5tb2R1bGUuZXhwb3J0cy5jaGVja05hbWVFeGlzdCA9ICgpID0+IHtcbiAgICBsZXQgY2FGb3JtID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNjYUZvcm1cIik7XG5cbiAgICBsZXQgYXBwTmFtZSA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKFwiI25hbWVcIik7XG4gICAgbGV0IGVycm9yUGFyID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoJyNuYW1lRXhpc3RFcnJvcicpO1xuXG4gICAgaWYoIWVycm9yUGFyLmNsYXNzTGlzdC5jb250YWlucygnaGlkZGVuJykpe1xuICAgICAgICBlcnJvclBhci5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKVxuICAgIH1cblxuICAgIC8vIGNoZWNrIGlmIHRoZSBhcHAgZXhpc3QgZm9yIHRoZSB1c2VyXG5cbiAgICBmZXRjaCgnL2FwaS9hcHA/bmFtZT0nK2FwcE5hbWUudmFsdWUsIHtcbiAgICAgICAgbWV0aG9kOiAnZ2V0JyxcbiAgICAgICAgY3JlZGVudGlhbHM6IFwiaW5jbHVkZVwiLFxuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgICBcImNvbnRlbnQtdHlwZVwiOiBcImFwcGxpY2F0aW9uL2pzb247IGNoYXJzZXQ9dXRmLThcIlxuICAgICAgICB9XG4gICAgfSkudGhlbigocmVzKT0+e1xuICAgICAgICBsZXQgZXJyb3JQYXIgPSBjYUZvcm0ucXVlcnlTZWxlY3RvcignI25hbWVFeGlzdEVycm9yJyk7XG4gICAgICAgIGxldCBjYUZvcm1TdWJtaXRCdG4gPSBjYUZvcm0ucXVlcnlTZWxlY3RvcignY2FGb3JtU3VibWl0QnRuJylcblxuICAgICAgICAvLyBpZiByZXMuc3RhdHVzIGlzIDIwMCB0aGVuIHNob3cgdGhlIGVycm9yIGVsc2UgaGlkZSB0aGUgZXJyb3JcbiAgICAgICAgaWYocmVzLnN0YXR1cyA9PT0gMjAwKXtcbiAgICAgICAgICAgIGVycm9yUGFyLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuICAgICAgICAgICAgY2FGb3JtU3VibWl0QnRuLmRpc2FibGVkID0gdHJ1ZTtcbiAgICAgICAgfSBlbHNlIGlmKHJlcy5zdGF0dXMgIT09IDIwMCAmJiAhZXJyb3JQYXIuY2xhc3NMaXN0LmNvbnRhaW5zKCdoaWRkZW4nKSkge1xuICAgICAgICAgICAgZXJyb3JQYXIuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgICAgICAgICBjYUZvcm1TdWJtaXRCdG4uZGlzYWJsZWQgPSBmYWxzZTtcbiAgICAgICAgfVxuICAgICAgICAvLyBjb25zb2xlLmxvZygxMjIyKVxuICAgIH0pLmNhdGNoKGVyciA9PiB7XG4gICAgICAgIC8vIGRvIG5vdGhpbmdcbiAgICB9KTtcbn07XG5cbm1vZHVsZS5leHBvcnRzLmNhRm9ybUpzU3RhcnRlciA9ICgpID0+IHtcblxuICAgIGxldCBhZGRBcHBMaW5rID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNhZGRBcHBcIik7XG4gICAgbGV0IGNhRm9ybUNsb3NlQnRuID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNjYUZvcm1DbG9zZUJ0blwiKTtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuICAgIGxldCBjYUZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NhRm9ybVwiKTtcblxuICAgIGxldCBtZXNzYWdlRGl2ID0gbW9kYWxCb3gucXVlcnlTZWxlY3RvcihcIiNtZXNzYWdlXCIpO1xuXG4gICAgLy8gaGFuZGxlIHRoZSBjbGljayBvZiB0aGUgYWRkIGFwcCBmb3JtXG4gICAgYWRkQXBwTGluay5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiB7XG4gICAgICAgIHRoaXMuc2hvd0NhRm9ybSgpO1xuICAgIH0pO1xuXG4gICAgLy8gaGFuZGxlIHRoZSBmb3JtIHN1Ym1pdFxuICAgIGNhRm9ybS5hZGRFdmVudExpc3RlbmVyKCdzdWJtaXQnLCB0aGlzLmhhbmRsZUNhRm9ybVN1Ym1pdCk7XG5cblxuICAgIGxldCBtZXNzYWdlRGl2Q2xvc2VCdG4gPSBtZXNzYWdlRGl2LnF1ZXJ5U2VsZWN0b3IoXCIuY2xvc2VcIik7XG4gICAgbWVzc2FnZURpdkNsb3NlQnRuLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcy5oaWRlTWVzc2FnZSk7XG5cbiAgICAvLyBzdG9wIHByb3BhZ2F0aW9uIG9mIHRoZSBjbGljayBldmVudFxuICAgIGNhRm9ybS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiBlLnN0b3BQcm9wYWdhdGlvbigpKTtcbiAgICBtZXNzYWdlRGl2LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKGUpID0+IGUuc3RvcFByb3BhZ2F0aW9uKCkpO1xuXG5cbiAgICAvLyBoYW5kbGUgdGhlIGNsaWNrIG9uIHRoZSBjbG9zZSBidXR0b24gb2YgdGhlIGZvcm1cbiAgICBjYUZvcm1DbG9zZUJ0bi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIHRoaXMuaGlkZUNhRm9ybSk7XG5cbiAgICAvLyBoaWRlIHRoZSBtb2RhbFxuICAgIG1vZGFsQm94LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKGUpID0+IG1vZGFsQm94LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpKTtcblxuICAgIGxldCBhcHBOYW1lID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoXCIjbmFtZVwiKTtcblxuICAgIGFwcE5hbWUuYWRkRXZlbnRMaXN0ZW5lcigna2V5dXAnLCB0aGlzLmNoZWNrTmFtZUV4aXN0KTtcbn07XG4iLCJcInVzZSBzdHJpY3RcIjtcblxubW9kdWxlLmV4cG9ydHMubm90aWZ5TW9kYWwgPSAobWVzc2FnZSkgPT4ge1xuICAgIGxldCBtb2RhbEJveCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjbW9kYWxDb250YWluZXJcIik7XG4gICAgbGV0IG1lc3NhZ2VEaWMgPSBtb2RhbEJveC5xdWVyeVNlbGVjdG9yKFwiI21lc3NhZ2VcIik7XG4gICAgbGV0IG1lc3NhZ2VDb250ZW50RGl2ID0gbWVzc2FnZURpYy5xdWVyeVNlbGVjdG9yKFwiLm1lc3NhZ2UtY29udGVudFwiKTtcblxuICAgIG1lc3NhZ2VDb250ZW50RGl2LmlubmVyVGV4dCA9IG1lc3NhZ2U7XG5cbiAgICBtZXNzYWdlRGljLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuICAgIG1vZGFsQm94LmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xufTtcblxubW9kdWxlLmV4cG9ydHMuaGlkZU1lc3NhZ2UgPSAoZSkgPT4ge1xuICAgIGxldCBtb2RhbEJveCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjbW9kYWxDb250YWluZXJcIik7XG4gICAgbGV0IG1lc3NhZ2VEaWMgPSBtb2RhbEJveC5xdWVyeVNlbGVjdG9yKFwiI21lc3NhZ2VcIik7XG5cbiAgICBtZXNzYWdlRGljLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgIG1vZGFsQm94LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuXG4gICAgZS5zdG9wUHJvcGFnYXRpb24oKTtcbn07XG4iXSwic291cmNlUm9vdCI6IiJ9