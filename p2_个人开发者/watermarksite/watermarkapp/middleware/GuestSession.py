from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpRequest,HttpResponse
import os
from django.conf import settings
from datetime import datetime


class CreateGuestSession:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        ssid = request.COOKIES.get('ssid')
        if not ssid:
            # 创建用户session
            sesh = SessionStore()
            sesh.create()
            sesh['limits'] = settings.UPLOAD_LIMITS
            sesh.save()

            # 把session挂在request中
            request.guest_session = sesh

            os.mkdir(f'{settings.BASE_DIR}/output/{sesh.session_key}')
            os.mkdir(f'{settings.BASE_DIR}/userupload/{sesh.session_key}')

            resp = self.get_response(request)  # 生成响应，送往下一个处理环节
            resp.set_cookie("ssid", sesh.session_key)  # 增加cookie中的ssid，就是session_key
            return resp

        # 已有session的用户，用以下方式处理
        request.guest_session = SessionStore(session_key=ssid)  # 同样的，把session挂在request中
        resp = self.get_response(request)

        return resp


class GuestUploadLimit:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        start_time = request.guest_session.get('start_time')

        # 记录间隔起始时间
        if not start_time:
            start_time = datetime.now().timestamp()
            request.guest_session['start_time'] = start_time
            request.guest_session.save()

        period = datetime.now().timestamp() - start_time  # 间隔时长

        # 如果超过设定的间隔，就恢复到上传限制数的初始值
        if period > settings.UPLOAD_INTERVAL:
            request.guest_session['limits'] = settings.UPLOAD_LIMITS
            request.guest_session['start_time'] = datetime.now().timestamp()
            request.guest_session.save()


        print('request.guest_session.keys',request.guest_session.keys())
        print('request.guest_session.values', request.guest_session.values())

        return self.get_response(request)


