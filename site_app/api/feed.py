#  Nikulin Vasily © 2021
import datetime

from flask_login import current_user, login_required, AnonymousUserMixin

from config import NEWS_PER_PAGE, icons
from data import db_session
from data.news import News, Theme
from tools.tools import send_response, fillJson, has_edit_permission
from tools.url import url
from . import socket, api


@socket.on('getNews')
@api.route('/api/news', methods=['GET'])
def getNews(json=None):
    if json is None:
        json = dict()
    event_name = 'getNews'
    fillJson(json, ['page', 'theme'])

    try:
        if json['page'] is None:
            page = 0
        else:
            page = int(json['page'])
    except ValueError:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Page number must be integer']
            }
        )

    if json['theme'] is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify the theme']
            }
        )

    theme = json['theme']

    db_sess = db_session.create_session()

    news = db_sess.query(News).order_by(News.date.desc()).filter(
        News.theme_title == theme
    ).all()
    end = True if len(news) <= (page + 1) * NEWS_PER_PAGE else False
    for n in news:
        if isinstance(current_user, AnonymousUserMixin):
            n.is_liked = False
        else:
            n.is_liked = str(current_user.id) in str(n.liked_ids).split(";")
    news = news[page * NEWS_PER_PAGE:(page + 1) * NEWS_PER_PAGE]
    n: News

    return send_response(
        event_name,
        {
            'message': 'Success',
            'news':
                [
                    {
                        'id': n.id,
                        'title': n.title,
                        'message': n.message,
                        'date': n.date.strftime('%d %b at %H:%M'),
                        'picture': n.picture,
                        'likes': 0 if n.liked_ids is None or n.liked_ids == ''
                        else len(str(n.liked_ids).split(';')),
                        'isLiked': n.is_liked
                    }
                    for n in news
                ],
            'editPermission': has_edit_permission(theme),
            'end': end
        }
    )


@socket.on('createNews')
@api.route('/api/news', methods=['POST'])
@login_required
def createNews(json=None):
    if json is None:
        json = dict()

    event_name = 'createNews'
    fillJson(json, ['title', 'message', 'imageUrl', 'theme'])

    db_sess = db_session.create_session()

    news = News(
        theme_title=json['theme'],
        title=json['title'],
        message=json['message'] or '',
        date=datetime.datetime.now(),
        picture=json['imageUrl']
    )

    db_sess.add(news)
    db_sess.commit()

    send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )

    theme_address = db_sess.query(Theme.address).filter(Theme.title == json['theme']).first()

    return send_response(
        'showNotifications',
        {
            'message': 'Success',
            'notifications': [
                {
                    'logoSource': icons['new_post'],
                    'header_up': 'Новая запись!',
                    'header_down': news.title,
                    'date': news.date.strftime('%d %B'),
                    'time': news.date.strftime('%H:%M'),
                    'message': news.message,
                    'redirectLink': f'{url(".feed", theme_address=theme_address)}#{news.id}'
                }
            ],
            'errors': []
        },
        broadcast=True, include_self=False
    )


@socket.on('editNews')
@api.route('/api/news', methods=['PUT'])
def editNews(json=None):
    if json is None:
        json = dict()

    event_name = 'editNews'
    fillJson(json, ['identifier', 'title', 'message', 'imageUrl', 'isLike', 'theme'])

    db_sess = db_session.create_session()

    if not json['identifier']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify identifier']
            }
        )

    news = db_sess.query(News).get(json['identifier'])

    if news is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['News not found']
            }
        )

    if news.theme == json['theme'] and not has_edit_permission(json['theme']) and \
            not json['isLike']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have permissions to edit this post.']
            }
        )
    elif json['isLike']:
        if news.liked_ids is None:
            news.liked_ids = ''
        news.liked_ids = str(news.liked_ids)
        if str(current_user.id) not in news.liked_ids.split(';'):
            liked_ids = [] if not news.liked_ids else news.liked_ids.split(';')
            likes = len(liked_ids) + 1
            news.liked_ids = ';'.join(liked_ids + [str(current_user.id)])
            is_liked = True
        else:
            liked_ids = news.liked_ids.split(';')
            likes = len(liked_ids) - 1
            liked_ids.remove(str(current_user.id))
            news.liked_ids = ';'.join(liked_ids)
            is_liked = False
        db_sess.merge(news)
        db_sess.commit()
        return send_response(
            event_name,
            {
                'message': 'Success',
                'likes': likes,
                'isLiked': is_liked,
                'errors': []
            }
        )

    news.title = json['title'] or news.title
    news.message = news.message if json['message'] is None else json['message']
    news.picture = json['imageUrl']

    db_sess.merge(news)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@socket.on('deleteNews')
@api.route('/api/news', methods=['DELETE'])
@login_required
def deleteNews(json=None):
    if json is None:
        json = dict()

    event_name = 'deleteNews'
    fillJson(json, ['identifier'])

    db_sess = db_session.create_session()

    if not json['identifier']:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['Specify identifier']
            }
        )

    news = db_sess.query(News).get(json['identifier'])

    if news is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['News not found']
            }
        )

    if news.theme == json['theme'] and not has_edit_permission(json['theme']):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have permissions to delete this post.']
            }
        )

    db_sess.delete(news)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )
