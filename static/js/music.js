document.addEventListener('DOMContentLoaded', function() {
    const likeImages = document.querySelectorAll('.like img');

    likeImages.forEach(function(likeImage) {
    likeImage.addEventListener('click', function() {
        if (likeImage.src.includes('heart.png')) {
        likeImage.src = 'images/mdi_heart-outline.png';
        } else {
        likeImage.src = 'images/mdi_heart.png';
        }
    });
    });
});

function moveurl(url) { 
    window.location.href = url;
} 
