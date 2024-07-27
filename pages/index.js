// open answers

const openButtons = document.querySelectorAll('.answers__open-button');
const answers = document.querySelectorAll('.answers__answer');

for (let ind = 0; ind < openButtons.length; ++ind) {
    openButtons[ind].addEventListener('click', function (event) {
        answers[ind].classList.toggle('answers__answer_opened');
        openButtons[ind].classList.toggle('answers__open-button_active');
    });
}

// adaptive product

const titleUmbrella = document.querySelectorAll('.product__title')[1];
const titleStation = document.querySelectorAll('.product__title')[0];

const imageUmbrella = document.querySelectorAll('.product__image')[1];
const imageStation = document.querySelectorAll('.product__image')[0];

const secondCardUmbrella = document.querySelectorAll('.product')[1].querySelectorAll('.product__card')[1];
const thirdCardStation = document.querySelectorAll('.product')[0].querySelectorAll('.product__card')[2];

const mediaQueryProduct = window.matchMedia('screen and (max-width: 800px)');

function productMobile() {
    titleUmbrella.after(imageUmbrella);
    titleStation.after(imageStation);
}

function productDesktop() {
    secondCardUmbrella.after(imageUmbrella);
    thirdCardStation.after(imageStation);
}

function mediaProduct(mediaQuery) {
    if (mediaQuery.matches) {
        productMobile();
    } else {
        productDesktop();
    }
}

mediaProduct(mediaQueryProduct);
mediaQueryProduct.addEventListener('change', mediaProduct);

// adaptive instruction

const instructionTitle = document.querySelector('.instruction__title');
const instructionImage = document.querySelector('.instruction__image');
const instruction = document.querySelector('.instruction__content');

const mediaQueryInstruction = window.matchMedia('screen and (max-width: 974px)');

function instructionMobile() {
    instructionTitle.after(instructionImage);
}

function instructionDesktop() {
    instruction.before(instructionImage);
}

function mediaInstruction(mediaQuery) {
    if (mediaQuery.matches) {
        instructionMobile();
    } else {
        instructionDesktop();
    }
}

mediaInstruction(mediaQueryInstruction);
mediaQueryInstruction.addEventListener('change', mediaInstruction);

// menu logic

const menuButton = document.querySelector('.header-mobile__menu-button');
const menu = document.querySelector('.menu');

menuButton.addEventListener('click', function (event) {
    menu.classList.add('menu_active');
});

const closeMenuButton = document.querySelector('.menu__close-button');

closeMenuButton.addEventListener('click', function (event) {
    menu.classList.remove('menu_active');
});

const menuLinks = document.querySelectorAll('.menu__link');

for (let ind = 0; ind < menuLinks.length; ++ind) {
    menuLinks[ind].addEventListener('click', function (event) {
        menu.classList.remove('menu_active');
    });

}