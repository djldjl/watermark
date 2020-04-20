# watermark
text watermark to picture
用Django实现给图片加文字水印
大体功能是：输入水印的文字，选择要加水印的图片，最后生成加好水印的图片供下载。
1、通过intercooler实现本页面内动态交互；
2、实现查看与下载历史图片功能（通过session\cookie）；
3、通过使用session\cookie\中间件， 实现限制上传次数的功能，即在一段时间内，不能超过规定次数上传文件。
