function addUnderline(element) {
    element.classList.add('underline');
  }
  
  function replaceImage(element) {
    var stars = element.parentNode.parentNode.getElementsByClassName('stars');
    var index = Array.prototype.indexOf.call(stars, element.parentNode);
  
    var cnt = 0;
    for (var i = 0; i < stars.length; i++) {
      var star = stars[i].firstElementChild;
      if (star.src.includes("pull-star.png")) {
        cnt++;
      }
    }
  
    if (cnt == index + 1) {
      for (var i = 0; i < stars.length; i++) {
        var star = stars[i].firstElementChild;
        star.src = "images/ph_star-bold.png";
      }
    } else {
      for (var i = 0; i <= index; i++) {
        var star = stars[i].firstElementChild;
        star.src = "images/pull-star.png";
      }
  
      for (var i = index + 1; i < stars.length; i++) {
        var star = stars[i].firstElementChild;
        star.src = "images/ph_star-bold.png";
      }
    }
  }
  