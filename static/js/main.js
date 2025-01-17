let menu =document.querySelector('.menu')
let siderbar =document.querySelector('.siderbar')
let mainContent =document.querySelector('.main--content')

menu.onclick=function(){
    siderbar.classList.toggle('active')
    mainContent.classList.toggle('active')
}