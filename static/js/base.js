function loader_function() {
    const lds_ripple_container = document.getElementById("lds-ripple-container");
    lds_ripple_container.style.display = "none";
    lds_ripple_container.style.opacity = "0%";
};
window.addEventListener("load", loader_function);

const search_bar_1 = document.getElementById("search-bar-1");
const search_button_1 = document.getElementById("search-button-1");
search_bar_1.style.display = "none";
search_button_1.type = "button";
if (search_bar_1.style.display == "none") {
    search_button_1.type = "button";
}
else {
    search_button_1.type = "submit";
}
function show_sb1() {
    if (search_bar_1.style.display == "none") {
        search_bar_1.style.display = "inline-block";
        search_button_1.type = "button";
    }
    else {
        search_bar_1.style.display = "none";
        search_button_1.type = "submit";
        if (search_bar_1.value == "") {
            search_button_1.type = "button";
        }
    }
};

const menu_button = document.querySelector(".menu-button");
const menu_drop_down = document.getElementById("menu-drop-down");
menu_button.addEventListener("click", () => {
    menu_button.classList.toggle("active");
    menu_drop_down.classList.toggle("active");
})
var window_limit_function = function() {
    if (window.innerWidth > 1000) {
        // me-remove toogle effect
        menu_button.classList.remove("active");
        menu_drop_down.classList.remove("active");
    }
};
window.addEventListener("resize", window_limit_function);
window.addEventListener("onload", window_limit_function);

function close_popup() {
    const popup_container = document.querySelector('.popup-container');
    popup_container.remove();
};