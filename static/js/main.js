// document.getElementById('demo').innerHTML = "This was created with Javascript"

// Show or hide password

var password_hash = document.getElementById("password_hash");
var password_hash2 = document.getElementById("password_hash2");
var show_password = document.getElementById("flexSwitchCheckDefault");
var show_pw_text = document.getElementById('show_pw_txt');
// var show_pw_text2 = document.getElementById('show_pw_txt2');
// var show_pw_text2 = document.getElementsByClassName('.form-check-label')

show_password.addEventListener('click', function(){
    if(password_hash.type ==='password'){
        password_hash.type = 'text';
        password_hash2.type = 'text';
        // show_pw_text2.innerHTML = 'Hide Password'
        show_pw_text.innerHTML = 'Hide Password'
    }else{
        password_hash.type = 'password';
        password_hash2.type = 'password';
        // show_pw_text2.innerHTML = 'show Password'
        show_pw_text.innerHTML = 'Show Password'


    }
});

