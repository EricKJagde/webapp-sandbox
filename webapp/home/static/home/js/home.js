function openForm() {
  alert("HI");
}

function floatToStyle(floatValue) {
  return Math.round(floatValue).toString() + "px";
}

function toggleSidenavVis() {
  var sidebarElement = document.getElementById("sidebar-id");
  if (!sidebarElement) {
    return;
  }
  var sideBarWidthStyle = "15%";

  /* See if the sidebar is active */
  var sidenavVisState = sidebarElement.style.width === sideBarWidthStyle;

  /* Get document elements */
  var navbarElement = document.getElementById("navbar-id");
  var mainElement = document.getElementById("main");
  var footerElement = document.getElementById("footer-id");

  if (sidenavVisState) {
    sidebarElement.style.width = "0";
    navbarElement.style.marginLeft = "0";
    mainElement.style.marginLeft = "0";
    footerElement.style.marginLeft = "0";
  }
  else {
    sidebarElement.style.width = sideBarWidthStyle;
    navbarElement.style.marginLeft = sideBarWidthStyle;
    mainElement.style.marginLeft = sideBarWidthStyle;
    footerElement.style.marginLeft = sideBarWidthStyle;
  }
}
