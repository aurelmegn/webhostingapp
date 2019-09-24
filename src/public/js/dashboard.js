(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["js/dashboard"],{

/***/ "./assets/js/dashboard.js":
/*!********************************!*\
  !*** ./assets/js/dashboard.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var notifyModal = function notifyModal(message) {
  var modalBox = document.querySelector("#modalContainer");
  var messageDic = modalBox.querySelector("#message");
  var messageContentDiv = messageDic.querySelector(".message-content");
  messageContentDiv.innerText = message;
  messageDic.classList.remove('hidden');
  modalBox.classList.remove('hidden');
};

var hideMessage = function hideMessage(e) {
  var modalBox = document.querySelector("#modalContainer");
  var messageDic = modalBox.querySelector("#message");
  messageDic.classList.add('hidden');
  modalBox.classList.add('hidden');
  e.stopPropagation();
};

var showCaForm = function showCaForm() {
  var caForm = document.querySelector("#caForm");
  var modalBox = document.querySelector("#modalContainer");
  modalBox.classList.remove('hidden');
  caForm.classList.remove('hidden');
};

var hideCaForm = function hideCaForm(e) {
  var caForm = document.querySelector("#caForm");
  var modalBox = document.querySelector("#modalContainer");
  caForm.reset();
  modalBox.classList.add('hidden');
  caForm.classList.add('hidden');
};

var handleCaFormSubmit = function handleCaFormSubmit(e) {
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
    if (res.status.toString().charAt(0) != '2') {
      // handle the error
      var errorPar = caForm.querySelector('#nameExistError');
      errorPar.classList.remove('hidden');
    } else {
      caForm.reset();
      hideCaForm();
      var message = "The application will be validated by an admin before any use";
      notifyModal(message); // messageDic.classList.remove("hidden");
    }
  })["catch"](function (err) {
    console.log(err.message);
    hideCaForm();
    notifyModal("An error occured, please try later");
  }); // e.preventDefault();
};

document.addEventListener('DOMContentLoaded', function () {
  var addAppLink = document.querySelector("#addApp");
  var caFormCloseBtn = document.querySelector("#caFormCloseBtn");
  var modalBox = document.querySelector("#modalContainer");
  var caForm = document.querySelector("#caForm");
  var messageDiv = modalBox.querySelector("#message"); // handle the click of the add app form

  addAppLink.addEventListener('click', function (e) {
    showCaForm();
  }); // handle the form submit

  caForm.addEventListener('submit', handleCaFormSubmit);
  var messageDivCloseBtn = messageDiv.querySelector(".close");
  messageDivCloseBtn.addEventListener('click', hideMessage); //

  caForm.addEventListener('click', function (e) {
    return e.stopPropagation();
  });
  messageDiv.addEventListener('click', function (e) {
    return e.stopPropagation();
  }); // handle the click on the close button of the form

  caFormCloseBtn.addEventListener('click', hideCaForm); // hide the modal

  modalBox.addEventListener('click', function (e) {
    return modalBox.classList.add('hidden');
  });
  var appName = caForm.querySelector("#name");
  var errorPar = caForm.querySelector('#nameExistError');
  appName.addEventListener('keyup', function () {
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
      }

      console.log(1222);
    })["catch"](function (err) {// do nothing
    });
  });
});

/***/ })

},[["./assets/js/dashboard.js","runtime"]]]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9hc3NldHMvanMvZGFzaGJvYXJkLmpzIl0sIm5hbWVzIjpbIm5vdGlmeU1vZGFsIiwibWVzc2FnZSIsIm1vZGFsQm94IiwiZG9jdW1lbnQiLCJxdWVyeVNlbGVjdG9yIiwibWVzc2FnZURpYyIsIm1lc3NhZ2VDb250ZW50RGl2IiwiaW5uZXJUZXh0IiwiY2xhc3NMaXN0IiwicmVtb3ZlIiwiaGlkZU1lc3NhZ2UiLCJlIiwiYWRkIiwic3RvcFByb3BhZ2F0aW9uIiwic2hvd0NhRm9ybSIsImNhRm9ybSIsImhpZGVDYUZvcm0iLCJyZXNldCIsImhhbmRsZUNhRm9ybVN1Ym1pdCIsInByZXZlbnREZWZhdWx0IiwiYXBwTmFtZSIsImFwcERlc2NyaXB0aW9uIiwiZmV0Y2giLCJtZXRob2QiLCJib2R5IiwiSlNPTiIsInN0cmluZ2lmeSIsIm5hbWUiLCJ2YWx1ZSIsImRlc2NyaXB0aW9uIiwiY3JlZGVudGlhbHMiLCJoZWFkZXJzIiwidGhlbiIsInJlcyIsInN0YXR1cyIsInRvU3RyaW5nIiwiY2hhckF0IiwiZXJyb3JQYXIiLCJlcnIiLCJjb25zb2xlIiwibG9nIiwiYWRkRXZlbnRMaXN0ZW5lciIsImFkZEFwcExpbmsiLCJjYUZvcm1DbG9zZUJ0biIsIm1lc3NhZ2VEaXYiLCJtZXNzYWdlRGl2Q2xvc2VCdG4iLCJjb250YWlucyIsImNhRm9ybVN1Ym1pdEJ0biIsImRpc2FibGVkIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQWE7O0FBRWIsSUFBSUEsV0FBVyxHQUFHLFNBQWRBLFdBQWMsQ0FBQ0MsT0FBRCxFQUFhO0FBQzNCLE1BQUlDLFFBQVEsR0FBR0MsUUFBUSxDQUFDQyxhQUFULENBQXVCLGlCQUF2QixDQUFmO0FBQ0EsTUFBSUMsVUFBVSxHQUFHSCxRQUFRLENBQUNFLGFBQVQsQ0FBdUIsVUFBdkIsQ0FBakI7QUFDQSxNQUFJRSxpQkFBaUIsR0FBR0QsVUFBVSxDQUFDRCxhQUFYLENBQXlCLGtCQUF6QixDQUF4QjtBQUVBRSxt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QUNDLE1BQUosS0FBZSxHQUFsQixFQUFzQjtBQUNsQkcsZ0JBQVEsQ0FBQzdCLFNBQVQsQ0FBbUJDLE1BQW5CLENBQTBCLFFBQTFCO0FBQ0FzQyx1QkFBZSxDQUFDQyxRQUFoQixHQUEyQixJQUEzQjtBQUNILE9BSEQsTUFHTyxJQUFHZixHQUFHLENBQUNDLE1BQUosS0FBZSxHQUFmLElBQXNCLENBQUNHLFFBQVEsQ0FBQzdCLFNBQVQsQ0FBbUJzQyxRQUFuQixDQUE0QixRQUE1QixDQUExQixFQUFpRTtBQUNwRVQsZ0JBQVEsQ0FBQzdCLFNBQVQsQ0FBbUJJLEdBQW5CLENBQXVCLFFBQXZCO0FBQ0FtQyx1QkFBZSxDQUFDQyxRQUFoQixHQUEyQixLQUEzQjtBQUNIOztBQUNEVCxhQUFPLENBQUNDLEdBQVIsQ0FBWSxJQUFaO0FBQ0gsS0FsQkQsV0FrQlMsVUFBQUYsR0FBRyxFQUFJLENBQ1o7QUFDSCxLQXBCRDtBQXFCSCxHQTVCRDtBQTZCSCxDQWhFRCxFIiwiZmlsZSI6ImpzL2Rhc2hib2FyZC5qcyIsInNvdXJjZXNDb250ZW50IjpbIlwidXNlIHN0cmljdFwiO1xuXG5sZXQgbm90aWZ5TW9kYWwgPSAobWVzc2FnZSkgPT4ge1xuICAgIGxldCBtb2RhbEJveCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjbW9kYWxDb250YWluZXJcIik7XG4gICAgbGV0IG1lc3NhZ2VEaWMgPSBtb2RhbEJveC5xdWVyeVNlbGVjdG9yKFwiI21lc3NhZ2VcIik7XG4gICAgbGV0IG1lc3NhZ2VDb250ZW50RGl2ID0gbWVzc2FnZURpYy5xdWVyeVNlbGVjdG9yKFwiLm1lc3NhZ2UtY29udGVudFwiKTtcblxuICAgIG1lc3NhZ2VDb250ZW50RGl2LmlubmVyVGV4dCA9IG1lc3NhZ2U7XG5cbiAgICBtZXNzYWdlRGljLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuICAgIG1vZGFsQm94LmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xufTtcblxubGV0IGhpZGVNZXNzYWdlID0gKGUpID0+IHtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuICAgIGxldCBtZXNzYWdlRGljID0gbW9kYWxCb3gucXVlcnlTZWxlY3RvcihcIiNtZXNzYWdlXCIpO1xuXG4gICAgbWVzc2FnZURpYy5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICBtb2RhbEJveC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcblxuICAgIGUuc3RvcFByb3BhZ2F0aW9uKCk7XG59O1xuXG5sZXQgc2hvd0NhRm9ybSA9ICgpID0+IHtcbiAgICBsZXQgY2FGb3JtID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNjYUZvcm1cIik7XG4gICAgbGV0IG1vZGFsQm94ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNtb2RhbENvbnRhaW5lclwiKTtcblxuICAgIG1vZGFsQm94LmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuICAgIGNhRm9ybS5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcblxuXG59O1xuXG5sZXQgaGlkZUNhRm9ybSA9IChlKSA9PiB7XG4gICAgbGV0IGNhRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjY2FGb3JtXCIpO1xuICAgIGxldCBtb2RhbEJveCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjbW9kYWxDb250YWluZXJcIik7XG5cbiAgICBjYUZvcm0ucmVzZXQoKTtcbiAgICBtb2RhbEJveC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICBjYUZvcm0uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59O1xuXG5cbmxldCBoYW5kbGVDYUZvcm1TdWJtaXQgPSAoZSkgPT4ge1xuICAgIGxldCBjYUZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NhRm9ybVwiKTtcblxuICAgIC8vIHNlbmQgdGhlIHJlcXVlc3RzIHRvIGNyZWF0ZSB0aGUgZm9ybVxuICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICBsZXQgYXBwTmFtZSA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKFwiI25hbWVcIik7XG4gICAgbGV0IGFwcERlc2NyaXB0aW9uID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoXCIjZGVzY3JpcHRpb25cIik7XG5cbiAgICBmZXRjaChcIi9hcGkvYXBwXCIsIHtcbiAgICAgICAgbWV0aG9kOiBcInBvc3RcIixcbiAgICAgICAgYm9keTogSlNPTi5zdHJpbmdpZnkoe25hbWU6IGFwcE5hbWUudmFsdWUsIGRlc2NyaXB0aW9uOiBhcHBEZXNjcmlwdGlvbi52YWx1ZX0pLFxuICAgICAgICBjcmVkZW50aWFsczogXCJpbmNsdWRlXCIsXG4gICAgICAgIGhlYWRlcnM6IHtcbiAgICAgICAgICAgIFwiY29udGVudC10eXBlXCI6IFwiYXBwbGljYXRpb24vanNvbjsgY2hhcnNldD11dGYtOFwiXG4gICAgICAgIH1cbiAgICB9KS50aGVuKChyZXMpID0+IHtcbiAgICAgICAgLy8gcmVzZXQgdGhlIGZvcm1cbiAgICAgICAgaWYocmVzLnN0YXR1cy50b1N0cmluZygpLmNoYXJBdCgwKSAhPSAnMicpe1xuICAgICAgICAgICAgLy8gaGFuZGxlIHRoZSBlcnJvclxuICAgICAgICAgICAgbGV0IGVycm9yUGFyID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoJyNuYW1lRXhpc3RFcnJvcicpO1xuICAgICAgICAgICAgZXJyb3JQYXIuY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG5cbiAgICAgICAgfSBlbHNlIHtcblxuICAgICAgICAgICAgY2FGb3JtLnJlc2V0KCk7XG4gICAgICAgICAgICBoaWRlQ2FGb3JtKCk7XG5cbiAgICAgICAgICAgIGxldCBtZXNzYWdlID0gXCJUaGUgYXBwbGljYXRpb24gd2lsbCBiZSB2YWxpZGF0ZWQgYnkgYW4gYWRtaW4gYmVmb3JlIGFueSB1c2VcIjtcbiAgICAgICAgICAgIG5vdGlmeU1vZGFsKG1lc3NhZ2UpO1xuICAgICAgICAgICAgLy8gbWVzc2FnZURpYy5jbGFzc0xpc3QucmVtb3ZlKFwiaGlkZGVuXCIpO1xuICAgICAgICB9XG5cbiAgICB9KS5jYXRjaCgoZXJyKSA9PiB7XG4gICAgICAgIGNvbnNvbGUubG9nKGVyci5tZXNzYWdlKTtcbiAgICAgICAgaGlkZUNhRm9ybSgpO1xuICAgICAgICBub3RpZnlNb2RhbChcIkFuIGVycm9yIG9jY3VyZWQsIHBsZWFzZSB0cnkgbGF0ZXJcIilcbiAgICB9KVxuXG4gICAgLy8gZS5wcmV2ZW50RGVmYXVsdCgpO1xufTtcblxuZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHtcblxuICAgIGxldCBhZGRBcHBMaW5rID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNhZGRBcHBcIik7XG4gICAgbGV0IGNhRm9ybUNsb3NlQnRuID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNjYUZvcm1DbG9zZUJ0blwiKTtcbiAgICBsZXQgbW9kYWxCb3ggPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI21vZGFsQ29udGFpbmVyXCIpO1xuICAgIGxldCBjYUZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NhRm9ybVwiKTtcblxuICAgIGxldCBtZXNzYWdlRGl2ID0gbW9kYWxCb3gucXVlcnlTZWxlY3RvcihcIiNtZXNzYWdlXCIpO1xuXG4gICAgLy8gaGFuZGxlIHRoZSBjbGljayBvZiB0aGUgYWRkIGFwcCBmb3JtXG4gICAgYWRkQXBwTGluay5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiB7XG4gICAgICAgIHNob3dDYUZvcm0oKTtcbiAgICB9KTtcblxuICAgIC8vIGhhbmRsZSB0aGUgZm9ybSBzdWJtaXRcbiAgICBjYUZvcm0uYWRkRXZlbnRMaXN0ZW5lcignc3VibWl0JywgaGFuZGxlQ2FGb3JtU3VibWl0KTtcblxuXG4gICAgbGV0IG1lc3NhZ2VEaXZDbG9zZUJ0biA9IG1lc3NhZ2VEaXYucXVlcnlTZWxlY3RvcihcIi5jbG9zZVwiKTtcbiAgICBtZXNzYWdlRGl2Q2xvc2VCdG4uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBoaWRlTWVzc2FnZSk7XG5cbiAgICAvL1xuICAgIGNhRm9ybS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiBlLnN0b3BQcm9wYWdhdGlvbigpKTtcbiAgICBtZXNzYWdlRGl2LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKGUpID0+IGUuc3RvcFByb3BhZ2F0aW9uKCkpO1xuXG5cbiAgICAvLyBoYW5kbGUgdGhlIGNsaWNrIG9uIHRoZSBjbG9zZSBidXR0b24gb2YgdGhlIGZvcm1cbiAgICBjYUZvcm1DbG9zZUJ0bi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGhpZGVDYUZvcm0pO1xuXG4gICAgLy8gaGlkZSB0aGUgbW9kYWxcbiAgICBtb2RhbEJveC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChlKSA9PiBtb2RhbEJveC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKSk7XG5cbiAgICBsZXQgYXBwTmFtZSA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKFwiI25hbWVcIik7XG4gICAgbGV0IGVycm9yUGFyID0gY2FGb3JtLnF1ZXJ5U2VsZWN0b3IoJyNuYW1lRXhpc3RFcnJvcicpO1xuXG4gICAgYXBwTmFtZS5hZGRFdmVudExpc3RlbmVyKCdrZXl1cCcsICgpID0+IHtcbiAgICAgICAgaWYoIWVycm9yUGFyLmNsYXNzTGlzdC5jb250YWlucygnaGlkZGVuJykpe1xuICAgICAgICAgICAgZXJyb3JQYXIuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJylcbiAgICAgICAgfVxuXG4gICAgICAgIC8vIGNoZWNrIGlmIHRoZSBhcHAgZXhpc3QgZm9yIHRoZSB1c2VyXG5cbiAgICAgICAgZmV0Y2goJy9hcGkvYXBwP25hbWU9JythcHBOYW1lLnZhbHVlLCB7XG4gICAgICAgICAgICBtZXRob2Q6ICdnZXQnLFxuICAgICAgICAgICAgY3JlZGVudGlhbHM6IFwiaW5jbHVkZVwiLFxuICAgICAgICAgICAgaGVhZGVyczoge1xuICAgICAgICAgICAgICAgIFwiY29udGVudC10eXBlXCI6IFwiYXBwbGljYXRpb24vanNvbjsgY2hhcnNldD11dGYtOFwiXG4gICAgICAgICAgICB9XG4gICAgICAgIH0pLnRoZW4oKHJlcyk9PntcbiAgICAgICAgICAgIGxldCBlcnJvclBhciA9IGNhRm9ybS5xdWVyeVNlbGVjdG9yKCcjbmFtZUV4aXN0RXJyb3InKTtcbiAgICAgICAgICAgIGxldCBjYUZvcm1TdWJtaXRCdG4gPSBjYUZvcm0ucXVlcnlTZWxlY3RvcignY2FGb3JtU3VibWl0QnRuJylcbiAgICAgICAgICAgIC8vIGlmIHJlcy5zdGF0dXMgaXMgMjAwIHRoZW4gc2hvdyB0aGUgZXJyb3IgZWxzZSBoaWRlIHRoZSBlcnJvclxuICAgICAgICAgICAgaWYocmVzLnN0YXR1cyA9PT0gMjAwKXtcbiAgICAgICAgICAgICAgICBlcnJvclBhci5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICAgICAgICAgICAgICBjYUZvcm1TdWJtaXRCdG4uZGlzYWJsZWQgPSB0cnVlO1xuICAgICAgICAgICAgfSBlbHNlIGlmKHJlcy5zdGF0dXMgIT09IDIwMCAmJiAhZXJyb3JQYXIuY2xhc3NMaXN0LmNvbnRhaW5zKCdoaWRkZW4nKSkge1xuICAgICAgICAgICAgICAgIGVycm9yUGFyLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgICAgICAgICAgIGNhRm9ybVN1Ym1pdEJ0bi5kaXNhYmxlZCA9IGZhbHNlO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgY29uc29sZS5sb2coMTIyMilcbiAgICAgICAgfSkuY2F0Y2goZXJyID0+IHtcbiAgICAgICAgICAgIC8vIGRvIG5vdGhpbmdcbiAgICAgICAgfSlcbiAgICB9KVxufSk7XG4iXSwic291cmNlUm9vdCI6IiJ9