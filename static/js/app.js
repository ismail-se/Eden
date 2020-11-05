// Event Listner
document.querySelector(".main").addEventListener("click", function () {
  const aside = document.querySelector("aside");
  const settings = document.querySelector(".settings");
  settings.classList.remove("show");
  var x = window.matchMedia("(max-width: 960px)");
  if (x.matches) {
    aside.classList.add("hide");
  }
});

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function settingsShow() {
  const settings = document.querySelector(".settings");
  settings.classList.toggle("show");
}

// Sidebar in and out
function sidebar() {
  const aside = document.querySelector("aside");
  const main = document.querySelector("main");
  const a = document.querySelector(".hamburger a");
  aside.classList.toggle("hide");

  var x = window.matchMedia("(min-width: 960px)");
  var y = window.matchMedia("(max-width: 960px)");

  if (x.matches) {
    main.classList.toggle("margin");
  }
}

// Counter
const counters = document.querySelectorAll(".counter");
const speed = 300;
const counter = counters.forEach((counter) => {
  const countUpdate = () => {
    const count = +counter.innerText;
    const target = +counter.getAttribute("data-target");

    let inc = 0;
    if (target >= 300) inc = target / speed;
    else inc = 1;

    if (count < target) {
      counter.innerText = Math.floor(count + inc);
      setTimeout(countUpdate, 1);
    } else {
      counter.innerText = target;
    }
  };
  countUpdate();
});

// var x = window.matchMedia("(max-width: 960px)");

// if (x.matches) {
//   sidebar();
// }

/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.querySelector("header").style.top = "0";
  } else {
    document.querySelector("header").style.top = "-5rem";
  }
  prevScrollpos = currentScrollPos;
};
