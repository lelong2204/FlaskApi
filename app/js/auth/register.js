var errors = {}

$(document).ready(function () {
    $('#register-form').on('submit', handleSubmit);

    $('#name').on('input',checkNameIsValid).blur(checkNameIsValid);
    $('#username').on('input',checkUsernameIsValid).blur(checkNameIsValid);
    $('#email').on('input',checkEmailIsValid).blur(checkEmailIsValid);
    $('#password').on('input',checkPasswordIsValid).blur(checkPasswordIsValid);
    $('#re_password').on('input',checkRePasswordIsValid).blur(checkRePasswordIsValid);
})

function checkNameIsValid() {
    var ele = $("#name-errors");
    var val = $('#name').val();
    errors.name = [];

    if (!val.trim().length) {
        errors.name.push("Name is required")
    } else {
        if (val.trim().length < 2) {
            errors.name.push("Name minimun is 2 characters")
        }
    }

    ele.empty();
    errors.name.map(d => {
        ele.append(`<li>${d}`)
    })
}

function checkUsernameIsValid() {
    var ele = $("#username-errors");
    var val = $('#username').val();
    errors.user_name = [];

    if (!val.length) {
        errors.user_name.push("Username is required")
    } else {
        if (hasWhiteSpace(val)) {
            errors.user_name.push("Username can't contain white space")
        }
    
        if (val.length < 8) {
            errors.user_name.push("Username minimun is 8 characters")
        }
    }

    ele.empty();
    errors.user_name.map(d => {
        ele.append(`<li>${d}`)
    })
}

function checkEmailIsValid() {
    var ele = $("#email-errors");
    ele.empty();
    var val = $('#email').val();
    errors.email = [];

    if (val.length) {
        if (!validateEmail(val)) {
            errors.email.push("Email is wrong format")
        }

        errors.email.map(d => {
            ele.append(`<li>${d}`)
        })
    }
}

function checkPasswordIsValid() {
    var ele = $("#password-errors");
    var pass = $('#password').val();
    var rePass = $('#re_password').val();
    errors.re_password = "";
    errors.password = [];

    if (!pass.length) {
        errors.password.push("Password is required")
    } else {
        var ele = $("#re_password-errors");
        ele.empty();
        if (rePass.length && pass !== rePass) {
            errors.re_password.push("Password and Confirm Password is not match");

            if (errors.re_password.length) {
                ele.append(`<li>${errors.re_password}`);
            }
        }

        if (hasWhiteSpace(pass)) {
            errors.password.push("Password can't contain white space")
        }

        if (pass.length < 8) {
            errors.password.push("Password minimun is 8 characters")
        }
    }

    ele.empty();
    errors.password.map(d => {
        ele.append(`<li>${d}`)
    })
}

function checkRePasswordIsValid() {
    var ele = $("#re_password-errors");
    var rePass = $('#re_password').val();
    var pass = $('#password').val();
    errors.re_password = "";
    if (!rePass.length) {
        errors.re_password = "Confirm Password is required";
    } else {
        if (pass !== rePass) {
            errors.re_password = "Password and Confirm Password is not match";
        }
    }

    ele.empty();
    if (errors.re_password.length) {
        ele.append(`<li>${errors.re_password}`)
    }
}

function hasWhiteSpace(str) {
    return str.indexOf(' ') >= 0
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function handleSubmit(e) {
    checkNameIsValid();
    checkUsernameIsValid();
    checkEmailIsValid();
    checkPasswordIsValid();
    checkRePasswordIsValid();
    for (var key in errors) {
        if (errors[key].length > 0) {
            return false
        }
    }
}