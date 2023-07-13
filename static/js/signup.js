var loginButton = document.getElementById('login-button');

function validateForm() {
    var username = document.querySelector('input[name="NICKNAME"]').value;
    var password = document.querySelector('input[name="PW"]').value;
    var passwordck = document.querySelector('input[name="PW-CK"]').value;
    var email = document.querySelector('input[name="EM"]').value;
  

    if (username === "" || password === "" || passwordck || email) {
      alert("공백없이 입력해주세요.");
      return false;
    }

    else{ 
        //로그인 성공
    }

  }