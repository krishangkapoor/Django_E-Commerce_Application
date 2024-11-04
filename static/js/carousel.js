function moveSlide(arrow, direction) {
    const carouselContainer = arrow.parentElement;
    const carousel = carouselContainer.querySelector('.carousel');
    const images = carousel.querySelectorAll('.carousel-image');
    const totalImages = images.length;

    const imageWidth = carouselContainer.clientWidth;
    let currentIndex = carousel.dataset.index ? parseInt(carousel.dataset.index) : 0;
    currentIndex += direction;

    if (currentIndex === totalImages) {
        carousel.style.transition = 'transform 0.5s ease';
        carousel.style.transform = `translateX(-${currentIndex * imageWidth}px)`;
        setTimeout(() => {
            carousel.style.transition = 'none';  
            carousel.style.transform = `translateX(0px)`;  
        }, 500);
        currentIndex = 0;  
    } 
    else if (currentIndex < 0) {
        carousel.style.transition = 'transform 0.5s ease';
        carousel.style.transform = `translateX(0px)`; 
        setTimeout(() => {
            carousel.style.transition = 'none';  
            carousel.style.transform = `translateX(-${(totalImages - 1) * imageWidth}px)`;  
        }, 500);
        currentIndex = totalImages - 1;  
    } 
    else {
        carousel.style.transition = 'transform 0.5s ease';
        carousel.style.transform = `translateX(-${currentIndex * imageWidth}px)`;
    }

    carousel.dataset.index = currentIndex;
}
