const open_menu = document.querySelector("#open-menu")
const navbar_list = document.querySelector("#navbar-list")

let nav_state = false


open_menu.addEventListener("click",OpenMenuHandler)




function OpenMenuHandler(){
    console.log(nav_state)
   if(nav_state){
    navbar_list.style.display = "none"
    nav_state = false
   }
   else{
    navbar_list.style.display = "flex"
    nav_state = true
   }
}



function setNav(resolution){
    if(resolution.matches){
        navbar_list.style.display = "flex"
        nav_state = false
    }
    else{
        navbar_list.style.display = "none"
        nav_state = false
    }
    
}

let desktop_resolution = window.matchMedia("(min-width:1000px)")

desktop_resolution.addEventListener('change',setNav)