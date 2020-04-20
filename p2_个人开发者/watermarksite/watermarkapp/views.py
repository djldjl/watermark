"""
python后端课程，实操作业：给图片加水印的 Django 实现
大体功能是：输入水印的文字，选择要加水印的图片，最后生成加好水印的图片供下载。
已实现基本功能，并实现查看与使用历史记录功能（通过session\cookie）；
通过使用session\cookie\中间件， 实现限制上传次数的功能，即在一段时间内，不能超过规定次数上传文件。
"""

from django.shortcuts import render
from django.http import HttpRequest, FileResponse,HttpResponseNotAllowed,HttpResponse
from wand.drawing import Drawing  # 加水印用
from wand.image import Image as WandImg # 加水印用
from PIL import Image,ImageFont,ImageDraw  # 加水印用
import uuid
import os
from django.conf import settings



# Create your views here.

def index(request: HttpRequest):
    return render(request, 'page.html')


def filehandler(request: HttpRequest):
    ssid = request.COOKIES.get("ssid")
    if not ssid:
        return HttpResponseNotAllowed("You can't touch this.")
    # 先判断是否达到文件上传数限制
    if request.guest_session.get('limits') <= 0:
        return HttpResponseNotAllowed("You can't touch this.")
    # 每次向'/file'提交文件可正常处理时，limits就会减1
    request.guest_session['limits'] -= 1
    if request.guest_session['limits'] < 0:    # 当limits小于0时，强制等于0
        request.guest_session['limits'] = 0
    request.guest_session.save()

    ori_img = request.FILES.get('ori_img')
    mark_text = request.POST.get('mark_text')  # 得用request.POST，因为form提交是用POST方式
    print('mark_text:', mark_text)
    result_file_path = f"{settings.BASE_DIR}/output/{ssid}/Toggle_{ori_img.name}"  # 打水印后的文件保存路径
    filename = 'Toggle_' + ori_img.name.split('.')[0]  # 打水印后的文件名称，不带后缀
    upload_file_path = f"{settings.BASE_DIR}/userupload/{ssid}/{ori_img.name}"  # 原始文件保存路径
    print('filename:', filename)

    with WandImg(file=ori_img) as background:
        # 先保存原始图片
        background.save(filename=upload_file_path)

        # 先把文字转为图片，再給背景图片上水印
        # 定义一些文字转图片的属性
        im_width = int(background.height * 0.8)    # 文字图片的宽度
        im = Image.new("RGBA", (im_width, int(im_width * 0.17)), (100, 100, 100, 100))  # 文字图片的大小、背景颜色（带透明度）
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype("Deng.ttf", int(30 * im_width / 300))   # 用了等线字体
        dr.text((5, 5), mark_text, font=font, fill="gray")
        # 保存文字图片当做水印图片
        temp_file_path = f"{settings.BASE_DIR}/userupload/{ssid}/{mark_text}_.png"
        im.save(temp_file_path)

        # 打水印
        with WandImg(filename=temp_file_path) as watermarker:
            background.watermark(watermarker, transparency=0.5, left=0, top=int(background.height * 0.4))
        background.save(filename=result_file_path)

    ctx = {'filename': filename}
    return render(request, 'item.html', context=ctx)


def download(request: HttpRequest):
    ssid = request.COOKIES.get("ssid")
    if not ssid:
        return HttpResponseNotAllowed("You can't touch this.")
    filename = request.GET.get('filename')
    file_path = f"{settings.BASE_DIR}/output/{ssid}/{filename}.jpg"
    print('marked_file_path:', file_path)
    resp = FileResponse(open(file_path, 'rb'))
    resp["content-type"] = "image/jpeg"
    resp["content-disposition"] = "attachment"
    return resp

def get_history(request:HttpRequest):
    ssid = request.COOKIES.get("ssid")
    if not ssid:
        return HttpResponseNotAllowed("You can't touch this.")
    files_path = f"{settings.BASE_DIR}/output/{ssid}/"
    filename_list = [n[:-4] for n in os.listdir(files_path)]   # 不带后缀的文件名列表
    print(filename_list)
    ctx = {"filename_list":filename_list}
    return render(request,'history_list.html',context=ctx)

def get_limits(request:HttpRequest):
    limits = request.guest_session.get('limits')
    # limits = req.guest_session["limits"]
    return HttpResponse(limits)

