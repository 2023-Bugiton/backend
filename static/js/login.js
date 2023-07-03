var loginButton = document.getElementById('login-button');

function validateForm() {
    var username = document.querySelector('input[name="ID"]').value;
    var password = document.querySelector('input[name="PW"]').value;

    if (username === "" || password === "") {
      alert("아이디와 비밀번호를 입력해주세요.");
      return false;
    }

    else{ 
        alert("로그인 성공");
    }

  }