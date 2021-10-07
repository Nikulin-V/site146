/*
 * Nikulin Vasily © 2021
 */

let news = Object()

news.get = function (theme,
                     page = 0,
                     fn = null) {
    if (fn)
        news.getFn = fn
    else
        news.getFn = null
    socket.emit('getNews', {
        'theme': theme,
        'page': page
    })
}

socket.on('getNews', function (data) {
    news.getJson = data
    if (news.getFn)
        news.getFn(data)
})


news.post = function (title = null,
                      message = null,
                      imageUrl = null,
                      theme = null,
                      fn = null) {
    if (fn)
        news.postFn = fn
    else
        news.postFn = null
    socket.emit('createNews', {
        'title': title,
        'message': message,
        'imageUrl': imageUrl,
        'theme': theme
    })
}

socket.on('createNews', function (data) {
    news.postJson = data
    if (news.postFn)
        news.postFn(data)
})


news.put = function (identifier = null,
                     title = null,
                     message = null,
                     imageUrl = null,
                     isLike = null,
                     theme = null,
                     fn = null) {
    if (fn)
        news.putFn = fn
    else
        news.putFn = null
    socket.emit('editNews', {
        'identifier': identifier,
        'title': title,
        'message': message,
        'imageUrl': imageUrl,
        'theme': theme,
        'isLike': isLike
    })
}

socket.on('editNews', function (data) {
    news.putJson = data
    if (news.putFn && data['message'] === 'Success')
        news.putFn(data)
    else if (data['message'] === 'Error') {
        showModal(createParagraph('Новость не найдена'))
        updatePage()
    }
})


news.delete = function (identifier = null,
                        theme = null,
                        fn = null) {
    if (fn)
        news.deleteFn = fn
    else
        news.deleteFn = null
    socket.emit('deleteNews', {
        'identifier': identifier,
        'theme': theme
    })
}

socket.on('deleteNews', function (data) {
    news.deleteJson = data
    if (news.deleteFn && data['message'] === 'Success')
        news.deleteFn(data)
    else if (data['message'] === 'Error') {
        showModal(createParagraph('Новость не найдена'))
        updatePage()
    }
})
