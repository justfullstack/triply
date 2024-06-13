"use script";
console.log("SLIDER JS Loaded...");


const sliders = document.querySelectorAll(`.slider`);


sliders.forEach((slider, i) => {
    slider.setAttribute("id", `slider--${i}`)

    let slides = document.querySelectorAll(`#slider--${i}>.slide`);
    let activeSlide = 0;
    let numSlides = slides.length;

    // mark dot as active
    // const activateDot = (slide_no ) => {
    //     document.querySelectorAll(`#slider--2>.dots>.dots__dot`)
    //     .forEach((dot) => {
    //         dot.classList.remove("dots__dot--active");
    //     });

    //     const activeDot = document.querySelector(`#slider--${i}>.dots__dot[data-slide="${slide_no}"]`);

    //     activeDot.classList.add("dots__dot--active");
    // }

    function goToSlide(slide) {
        slides.forEach((s, i) => {
            s.style.transform = `translateX(${(i - slide) * 100}%)`;
            // activateDot(slide);
        });
    }

    // init
    goToSlide(0);


    const nextSlide = function () {
        // on reaching end of slides, reset
        if (activeSlide === (numSlides - 1)) {
            activeSlide = 0;

        } else {
            // go to next slide
            activeSlide++;

        }

        goToSlide(activeSlide);
        // activateDot(activeSlide);

    }

    const prevSlide = function () {
        // on reaching start of slides, reset
        if (activeSlide === 0) {
            activeSlide = numSlides - 1;

        } else {
            // go to next slide
            activeSlide--;

        }
        goToSlide(activeSlide);
        // activateDot(activeSlide);
    }



    if (numSlides > 1) {
        let btnPrev = document.querySelector(`#slider--${i}>.slider__buttons>.slider__btn--left`);
        let btnNext = document.querySelector(`#slider--${i}>.slider__buttons>.slider__btn--right`);
        let dotsContainer = document.querySelector(`#slider--${i}>.dots`);


        slides.forEach((slide, index) => {

            // arrange all slides in a line
            slide.style.transform = `translateX(${index * 100}%)`;
            slide.style.height = "100%";

            // create a dot for each slide
            // dotsContainer.insertAdjacentHTML('beforeend', `<button class="dots__dot" data-slide=${i}></button>`)
        })


        // use arrow clicks to move between slides
        btnNext.addEventListener('click', nextSlide);
        btnPrev.addEventListener('click', prevSlide);

        // use buttons for navigation

        document.addEventListener('keydown', (e) => {
            // using short circuiting
            e.key === "ArrowRight" && nextSlide();
            e.key === "ArrowLeft" && prevSlide();
        });

        console.log(numSlides);

    } else {
        console.log(numSlides);
        console.log("Only one slide here");
        return;
    }





});


console.log("slider js loaded");


