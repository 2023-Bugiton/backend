document.addEventListener("DOMContentLoaded", function() {
    const heart = document.querySelector(".heart img");
    let isLiked = false;

    heart.addEventListener("click", function() {
        if (isLiked) {
            heart.src = "images/mdi_heart-outline.png";
            isLiked = false;
        } else {
            heart.src = "images/mdi_heart.png";
            isLiked = true;
        }
    });
});