//  Nikulin Vasily © 2021

function resetPassword(email) {
    $('.auth-modal').remove()
    let message =
        `<div class="form-floating">
            <input id="email-reset" class="form-control" type="email" value="${email}" placeholder="Email">
            <label for="title-input">Email</label>
        </div>`
    let button = `<button id="send-code" onclick="sendEmail()" class="btn btn-info">Отправить код</button>`
    showModal(message, 'Сброс пароля', [button])
}

function sendEmail() {
    $('.reset-error').remove();
    $('#email-reset').removeClass('is-invalid')
    $('#send-code').addClass('disabled')
    $('.modal-footer').prepend(`<div class="spinner-border text-info" role="status"></div>`)

    sendCode()
}

function errorMessage(text) {
    $('.spinner-border').remove()
    return `<div class="reset-error alert alert-danger" role="alert" style="margin-top: 20px">
                ${text}
            </div>`
}

function successMessage(text) {
    $('.spinner-border').remove()
    return `<div class="reset-error alert alert-success" role="alert" style="margin-top: 20px">
                ${text}
            </div>`
}

function sendCode() {
    let email = $('#email-reset')
    if (validateEmail(email.val()))
        socket.emit('sendCode', {email: email.val()})
    else {
        email.addClass("is-invalid")
        $('.modal-body').append(errorMessage('Проверьте правильность введённого email'))
    }

}

socket.on('sendCode', function (data) {
    console.log(data)
    if (data['message'] === 'Error' && $('.reset-error').length === 0)
        $('.modal-body').append(
            errorMessage('Пользователь с указанным email не зарегистрирован'))
    if (data['message'] === 'Success')
        $('.modal-body').append(
            successMessage('Новый пароль отправлен на Вашу почту'))
})

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}