#  Nikulin Vasily © 2021
from flask import render_template, redirect, request

from site_app import site
from tools.url import url


@site.app_errorhandler(400)
@site.app_errorhandler(401)
@site.app_errorhandler(403)
@site.app_errorhandler(404)
@site.app_errorhandler(408)
@site.app_errorhandler(413)
@site.app_errorhandler(415)
@site.app_errorhandler(500)
def error_handler(error):
    return redirect(url(".error_page") + f"?code={error.code}")


global_messages = {
    400: ['Некорректный запрос',
          'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
          'техподдержку'],
    401: ['Вы не вошли в систему',
          'Через несколько секунд Вы будете направлены на страницу авторизации'],
    403: ['Доступ запрещён',
          'Данный ресурс недоступен для вашего типа учетной записи. <br>'
          'Если Вы считаете иначе - напишите нам на support@area-146.tk'],
    404: ['Страница не найдена',
          'Проверьте правильность введённого адреса'],
    408: ['Превышено время ожидания',
          'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
          'техподдержку'],
    413: ['Превышен размер файла',
          'Попробуйте загрузить файл поменьше'],
    415: ['Неподдерживаемый формат файла',
          'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
          'техподдержку'],
    500: ['Ошибка на стороне сайта',
          'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
          'техподдержку'],
}


@site.route("/error")
def error_page():
    code = request.args.get("code")

    if code is None:
        code = 404
    else:
        code = int(code)

    if code not in global_messages.keys():
        code = 404

    return render_template('site/error_page.html',
                           code=code,
                           title=global_messages[code][0],
                           message=global_messages[code][1]), code
