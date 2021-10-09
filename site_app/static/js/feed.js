/*
 * Nikulin Vasily © 2021
 */

users.hasEditPermission(theme(), showCreatePostButton)

function showCreatePostButton() {
    if (users.editor === true) {
        createPostButton = `<td style="text-align: right">
                                <button id="create-news" class="btn btn-info" onclick="createNews()">
                                    Создать пост
                                </button>
                            </td>`
        $("#news-header > table > tbody > tr").append(createPostButton)
    }
}

users.isAuthorized()

updatePage()
html = document.getElementsByTagName('html')[0]
window.addEventListener('scroll', function () {
    let height = Math.max(document.body.scrollHeight, document.body.offsetHeight,
        html.clientHeight, html.scrollHeight, html.offsetHeight)
    if (pageYOffset + window.innerHeight + 1 >= height) {
        addNews(k, false)
    }
})

function updatePage(isFullUpdate = true) {
    k = 0
    was_end = false
    addNews(k, isFullUpdate)
}

main = document.getElementsByTagName('main')[0]

function addNews(page = 0, isFullUpdate = true) {
    if (!was_end) {
        news.get(theme(), page, function (data) {
            if (isFullUpdate) {
                main = document.getElementsByTagName('main')[0]
                while (document.getElementsByClassName('news').length > 0)
                    main.removeChild(document.getElementsByClassName('news')[0])
            }
            if (data['news'].length > 0) {
                const newsList = data['news']
                for (newsId = 0; newsId < newsList.length; newsId++) {
                    const n = Object(newsList[newsId])
                    if (n.picture)
                        picture = `<img id="${n.id}-picture" src="${n.picture}" alt="Неверная ссылка на изображение новости" class="card-img-top" ${isMobile() ? '' : 'style="width: 55%; align-self: center"'}>`
                    else
                        picture = ''
                    if (data['editPermission'] && users.authorized) {
                        authorButtons = `
                                <div style="display: inline-flex">
                                    <button onclick="deleteNews('${n.id}')" class="btn btn-outline-danger btn-delete btn-icon"><span class="material-icons md-red">clear</span></button>
                                    <button onclick="editNews('${n.id}')" class="btn btn-outline-warning btn-edit btn-icon"><span class="material-icons-round md-yellow">edit</span></button>
                                </div>`
                    } else authorButtons = ''
                    likes = parseInt(n.likes) > 0 ? " " + n.likes.toString() : ""
                    likeButton = `<td style="text-align: right; border: 0; width: 1px">
                                    <button id="${n.id}-like" onclick="like('${n.id}')" class="btn btn-outline-danger btn-like btn-icon">
                                        <span id="${n.id}-like-symbol" class="material-icons-round md-red">favorite${n.isLiked ? "" : "_border"}</span>
                                        <span id="${n.id}-like-counter" class="btn-icon-text">${likes}</span>
                                    </button>
                                </td>`
                    newsFooter = `
                        <table style="width: 100%; border: 0; margin: 5px 0">
                            <tr style="border: 0">
                                <td style="text-align: left; border: 0; width: 1%">
                                    ${authorButtons}
                                </td>
                                <td style="border: 0">
                                    <p style="margin-bottom: 0;${isMobile() ? " font-size: .9em;" : ""} text-align: center; position: relative">
                                        <small class="text-muted">${n.date}</small>
                                    </p>
                                </td>
                                    ${users.authorized === true ? likeButton : ''}
                            </tr>
                        </table>
                    `
                    main.innerHTML += `
                            <div class="news" id="${n.id}">
                                <div class="card mb-3">
                                    ${picture}
                                    <div class="card-body">
                                        <h5 class="card-title" id="${n.id}-title">${n.title}</h5>
                                        <p class="card-text" id="${n.id}-text">${n.message}</p>
                                    </div>
                                    <div class="card-footer">
                                        ${newsFooter}
                                    </div>
                                </div>
                            </div>
                        `
                }
            } else {
                was_end = true
                if (k === 0)
                    main.insertAdjacentHTML('beforeend',
                        `
                        <div class="card news">
                            <div class="card-body">
                                <h5 class="card-title" style="text-align: center">Новостей нет</h5>
                                <p class="card-text" style="text-align: center">Рано или поздно они точно появятся, но сейчас их нет(</p>
                            </div>
                        </div>
                    `)
            }
            k += 1
        })
    }
}

function createNews() {
    message =
        `<div>
            <div class="form-floating">
                <input id="title-input" class="form-control" placeholder="Заголовок" onclick="valid(this)" autocomplete="off">
                <label for="title-input">Заголовок</label>
            </div>
            <br>
            <div class="form-floating">
                <textarea id="text-input" class="form-control" placeholder="Текст"></textarea>
                <label for="text-input">Текст</label>
            </div>
            <br>
            <div class="form-floating">
                <input type="url" id="image-input" name="illustration" class="form-control" placeholder="Изображение" autocomplete="off">
                <label for="image-input">Ссылка на изображение</label>
            </div>
        </div>`
    button = document.createElement('button')
    button.textContent = "Опубликовать"
    button.className = "btn btn-info"

    progressBarBack = document.createElement('div')
    progressBarBack.className = "progress"
    progressBar = document.createElement('div')
    progressBarBack.appendChild(progressBar)
    progressBar.className = "progress-bar progress-bar-striped progress-bar-animated btn-info"
    progressBar.setAttribute("role", "progressbar")
    progressBar.setAttribute("aria-valuemin", "0")
    progressBar.setAttribute("aria-valuemax", "0")
    progressBar.setAttribute("aria-valuenow", "0")
    progressBarBack.style.width = "100%"
    progressBar.style.width = "0%"
    progressBarBack.style.display = "none"


    button.onclick = function () {
        const title = $('#title-input').val()
        const text = $('#text-input').val()
        const imageUrl = $('#image-input').val()
        if (title) {
            k = 0
            news.post(title, text, imageUrl, theme(), updatePage)
            closeModal()
        } else document.getElementById('title-input').classList.add('is-invalid')
    }
    showModal(message, 'Новый пост', [button, progressBarBack])
}

function editNews(id) {
    id = id.toString()
    const titleElement = document.getElementById(id + "-title")
    const title = titleElement.textContent
    const textElement = document.getElementById(id + "-text")
    if (textElement)
        text = textElement ? textElement.textContent : ''
    const imageUrl = $('#' + id + '-picture').attr('src')
    message =
        `<div>
            <div class="form-floating">
                <input id="title-input" class="form-control" placeholder="Заголовок" value="${title}" onclick="valid(this)" autocomplete="off">
                <label for="title-input">Заголовок</label>
            </div>
            <br>
            <div class="form-floating">
                <textarea id="text-input" class="form-control" placeholder="Текст">${text}</textarea>
                <label for="text-input">Текст</label>
            </div>
            <br>
            <div class="form-floating">
                <input type="url" id="image-input" name="illustration" class="form-control" placeholder="Изображение" value="${imageUrl !== undefined ? imageUrl : ''}" autocomplete="off">
                <label for="image-input">Ссылка на изображение</label>
            </div>
            <br>
        </div>`
    button = document.createElement('button')
    button.textContent = "Сохранить"
    button.className = "btn btn-info"

    progressBarBack = document.createElement('div')
    progressBarBack.className = "progress"
    progressBar = document.createElement('div')
    progressBarBack.appendChild(progressBar)
    progressBar.className = "progress-bar progress-bar-striped progress-bar-animated btn-info"
    progressBar.setAttribute("role", "progressbar")
    progressBar.setAttribute("aria-valuemin", "0")
    progressBar.setAttribute("aria-valuemax", "0")
    progressBar.setAttribute("aria-valuenow", "0")
    progressBarBack.style.width = "100%"
    progressBar.style.width = "0%"
    progressBarBack.style.display = "none"

    btnClear = document.createElement("clear-image")
    btnClear.textContent = "Удалить изображение"
    btnClear.className = "btn btn-info"
    btnClear.onclick = () => {
        news.put(id, null, null, "!clear", null, null, updatePage)
        closeModal()
    }

    button.onclick = () => {
        const newTitle = $('#title-input').val()

        if (newTitle) {
            const newText = $('#text-input').val()
            const newImageUrl = $('#image-input').val()
            news.put(id, newTitle, newText, newImageUrl, null, theme(), updatePage)
            closeModal()
        } else document.getElementById('title-input').classList.add('is-invalid')
    }
    showModal(message, 'Изменение поста', [button])
}

function deleteNews(id) {
    news.delete(id, theme(), updatePage)
}

function like(id) {
    news.put(id, null, null, null, true, null, function (data) {
        let likeSymbol = document.getElementById(id + "-like-symbol")
        let likeCounter = document.getElementById(id + "-like-counter")

        if (data["isLiked"]) {
            likeSymbol.textContent = "favorite"
        } else {
            likeSymbol.textContent = "favorite_border"
        }

        if (data["likes"] === 0) {
            likeCounter.textContent = ""
        } else {
            likeCounter.textContent = data["likes"].toString()
        }
    })
}

function valid(element) {
    if (element.classList.contains("is-invalid")) {
        element.classList.remove("is-invalid")
    }
}

function showNewPosts() {
    let newPostsBtn = document.getElementById('news-update-btn')
    updatePage();
    newPostsBtn.style.display = 'none';
    let usernameBtn = document.getElementById('username')
    usernameBtn.scrollIntoView()
}

function showNewPostsBtn() {
    document.getElementById('news-update-btn').style.display = "block"
}
