/* toggle memu */
let menu = document.querySelector('#menu-btn');
let icon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.accordion_menu');
let aside = document.querySelector('.sidebar');
let  asideOpen = document.querySelector('#aside-menu-btn');
let  asidelose = document.querySelector('.close-aside');


menu.onclick = () => {
    icon.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

/* window.onscroll = () => {
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
} */
/* toggle memu */

// ACCORDION START
let listElements = document.querySelectorAll('.link');

listElements.forEach(listElement => {
    listElement.addEventListener('click', ()=>{
        if (listElement.classList.contains('active')){
            listElement.classList.remove('active');
        }else{
            listElements.forEach (listE => {
                listE.classList.remove('active');
            })
            listElement.classList.toggle('active');
        }
    })
});
//ACCORDION END

// Aside control START
let asideControl = document.querySelectorAll('.aside-control');

asideControl.forEach(listElement => {
    listElement.addEventListener('click', ()=>{
        if (listElement.classList.contains('aside-menu-btn')){
            aside.classList.toggle('mobile-aside');
        }
        else if (listElement.classList.contains('close-aside')){
            aside.classList.remove('mobile-aside');
        }
    })
});
//Aside control END


/* SLIDER CODE*/
const carousel = document.querySelector(".carousel"),
firstImg = carousel.querySelectorAll("img")[0],
arrowIcons = document.querySelectorAll(".coursel-wrapper i");

let isDragStart = false, isDragging = false, prevPageX, prevScrollLeft, positionDiff;

const showHideIcons = () => {
    // showing and hiding prev/next icon according to carousel scroll left value
    let scrollWidth = carousel.scrollWidth - carousel.clientWidth; // getting max scrollable width
    arrowIcons[0].style.display = carousel.scrollLeft == 0 ? "none" : "block";
    arrowIcons[1].style.display = carousel.scrollLeft == scrollWidth ? "none" : "block";
}

arrowIcons.forEach(icon => {
    icon.addEventListener("click", () => {
        let firstImgWidth = firstImg.clientWidth + 14; // getting first img width & adding 14 margin value
        // if clicked icon is left, reduce width value from the carousel scroll left else add to it
        carousel.scrollLeft += icon.id == "left" ? -firstImgWidth : firstImgWidth;
        setTimeout(() => showHideIcons(), 60); // calling showHideIcons after 60ms
    });
});

const autoSlide = () => {
    // if there is no image left to scroll then return from here
    if(carousel.scrollLeft - (carousel.scrollWidth - carousel.clientWidth) > -1 || carousel.scrollLeft <= 0) return;

    positionDiff = Math.abs(positionDiff); // making positionDiff value to positive
    let firstImgWidth = firstImg.clientWidth + 14;
    // getting difference value that needs to add or reduce from carousel left to take middle img center
    let valDifference = firstImgWidth - positionDiff;

    if(carousel.scrollLeft > prevScrollLeft) { // if user is scrolling to the right
        return carousel.scrollLeft += positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
    }
    // if user is scrolling to the left
    carousel.scrollLeft -= positionDiff > firstImgWidth / 3 ? valDifference : -positionDiff;
}

const dragStart = (e) => {
    // updatating global variables value on mouse down event
    isDragStart = true;
    prevPageX = e.pageX || e.touches[0].pageX;
    prevScrollLeft = carousel.scrollLeft;
}

const dragging = (e) => {
    // scrolling images/carousel to left according to mouse pointer
    if(!isDragStart) return;
    e.preventDefault();
    isDragging = true;
    carousel.classList.add("dragging");
    positionDiff = (e.pageX || e.touches[0].pageX) - prevPageX;
    carousel.scrollLeft = prevScrollLeft - positionDiff;
    showHideIcons();
}

const dragStop = () => {
    isDragStart = false;
    carousel.classList.remove("dragging");

    if(!isDragging) return;
    isDragging = false;
    autoSlide();
}

carousel.addEventListener("mousedown", dragStart);
carousel.addEventListener("touchstart", dragStart);

document.addEventListener("mousemove", dragging);
carousel.addEventListener("touchmove", dragging);

document.addEventListener("mouseup", dragStop);
carousel.addEventListener("touchend", dragStop);




// SEE MORE DROP DOWN
let wraper = document.querySelectorAll('.past_series_item_container');
let btn = document.querySelector('.seriesbtn');

let currentimg = 1; //
btn.addEventListener('click', function () {
    for(let i = currentimg; i < currentimg +2; i++) {  //+2
        if (wraper[i]) {
            wraper[i].style.display = 'flex';
        }
    }

    currentimg += 1;
    if (currentimg >= wraper.length) {
        event.target.style.display="none";
   }
}); 

// SEE MORE DROP DOWN END