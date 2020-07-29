function setCookie(cname, cvalue) {
  var d = new Date();
  d.setTime(d.getTime() + (365 * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;samesite=strict";
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(";");
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function isOnMobile() {
  let check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};

function addDot(parent) {
  if (getCookie("theme") == "light") {
    return;
  }
  dot = document.createElement("div");
  dot.classList.add("theme_dot");
  dot.style.position = "absolute";
  var height = window.innerHeight - 20
  var width = window.innerWidth - 20
  dot.style.top = ((height * Math.random()) + 10) + "px";
  dot.style.left = ((width * Math.random()) + 10) + "px";
  dot.style.height = "2px";
  dot.style.width = "2px";
  dot.style.background = "#fff";
  document.body.appendChild(dot);
}

function darkTheme() {
  document.body.style.background = "#000";
  document.body.classList.add("darkTheme");
  var wrapper = document.getElementById("documentwrapper");
  var pagesize = window.innerWidth * window.innerHeight;
  var dots = pagesize / 900;
  for (var i = 0; i < dots; i++) {
    setTimeout(function () {
      addDot(wrapper);
    }, 1);
  }
}

function lightTheme() {
  document.body.classList.remove("darkTheme");
  document.body.style.backgroundImage = "linear-gradient(#f666aa, #f3d77e)";
  document.body.style.backgroundRepeat = "no-repeat";
  document.body.style.backgroundAttachment = "fixed";
}

function clearDots() {
  var dots = document.getElementsByClassName("theme_dot");
  while (dots[0]) {
    dots[0].parentNode.removeChild(dots[0]);
  }
}

function drawTheme() {
  clearDots();
  theme = getCookie("theme");
  if (theme == "dark") {
    darkTheme();
  } else {
    lightTheme();
  }
}

function switchTheme() {
  clearDots();
  theme = getCookie("theme");
  if (theme == "dark") {
    setCookie("theme", "light");
    lightTheme();
  } else {
    setCookie("theme", "dark");
    darkTheme();
  }
}

function setupImages() {
  modal = document.getElementById("modal");
  full = document.getElementById("full-img");
  modal.onclick = function() {modal.style.display = "none"};
  images = document.getElementById("document").getElementsByTagName("img");
  if (!images[0]) {
      return;
  }
  image_wrapper = document.createElement("div");
  image_wrapper.classList.add("image-wrapper");
  images[0].parentNode.appendChild(image_wrapper);
  for (i = 0; i < images.length; i++) {
    images[i].title = images[i].alt;
    images[i].parentNode.style.display = "inline";
    images[i].onclick = showImageClosure(images[i], modal, full);
    image_wrapper.appendChild(images[i]);
  }
}

function showImageClosure(image, modal, full) {
    return function () {
        showImage(image, modal, full);
    };
}

function showImage(image, modal, full) {
  modal.style.display = "block";
  full.src = image.src;
  full.title = image.title;
}

window.onload = function() {
  if (isOnMobile()) {
    old = document.getElementById("stylesheet").href;
    document.getElementById("stylesheet").href = old.replace("style.css", "mobile.css");
  }
  drawTheme();
  setupImages();
  var button = document.getElementById("theme_button");
  button.onclick = this.switchTheme;
};

window.onresize = drawTheme;
