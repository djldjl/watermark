from dominate.document import document
import dominate.tags as dom


# 一些元素的cls
CENTERFRAME = "flex flex-col items-center justify-center bg-teal-200 h-screen"
HISTORYBTN = "flex flex-row items-center justify-between bg-gray-200 shadow-xl p-2 rounded-lg w-80 h-auto"
HISTORY_ICON = "fas fa-history text-gray-600 font-medium text-lg mr-3"
UPLOAD_FORM_ATTRIS ={
    "class":"flex flex-col justify-center",
    "ic-post-to": "/file",
    "ic-target": "#result_item",
    "ic-replace-target": "true",
    "enctype": "multipart/form-data"
}
CARD1 = "flex flex-col bg-green-400 shadow-xl p-1 rounded-lg w-80 h-auto"
TEXT_INPUT = "shadow border rounded m-1 p-1 text-base text-center font-thin"
CARD2 = "flex flex-col bg-white shadow-xl p-2 rounded-lg w-80 h-80"
DASHED_BOX = "flex flex-col items-center justify-center border-dashed border-2 border-gray-200 h-full"
UPLOAD_ICON = "fas fa-file-upload text-gray-300 font-medium text-6xl"
UPLOAD_BUTTON = "flex justify-center bg-green-400 px-3 py-2 mt-4 text-white rounded shadow"
RESULT_CONTAINER = "flex flex-col bg-white items-center"
RESULT_ITEM = "flex flex-row items-center justify-between bg-gray-700 p-2 border-t border-gray-600 w-64"
HISTORY_ITEM = "flex flex-row items-center justify-between bg-white p-2 w-auto"


# 为了写head部分的引入方便，写个link_函数；下面script_函数类似
def link_(lk):
    return dom.link(rel="stylesheet",type="text/css",href=lk)

def script_(s):
    return dom.script(src=s)

def page():
    doc = document()
    with doc.head:
        link_("https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css")  # tailwind
        link_("https://extra-uru1z3cxu.now.sh/css/extra.css")  # 额外写的扩展库
        link_("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.css")  # 为了使用font-awesome的图标
        link_("https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.css")  # modal
        script_("https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js") # jquery
        script_("https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.js")  # modal
        script_("{% static 'intercooler-1.2.2.js' %}")   # intercooler
    with doc.body:
        with dom.div(cls=CENTERFRAME) as CenterFrame:
            with dom.div(cls=HISTORYBTN) as HistoryBtn:
                with dom.div():
                    dom.span("Upload limits:",cls="text-base font-normal text-gray-700")
                    dom.span({
                        "ic-src":"/limits",
                        "ic-poll":"2s",
                        "class":"text-base font-normal text-gray-700 mr-5"
                    })
                # dom.p("Upload History",cls="text-base font-normal text-gray-700 mr-5" )
                with dom.a({
                    "href":"#ex1",
                    "rel":"modal:open",
                    "ic-get-from":"/history",   # 从"/history"获取资源
                    "ic-target":"#history_content",   # 在#history_content展示
                }):
                    dom.i(cls=HISTORY_ICON)
            with dom.div(id="ex1",cls="modal"):
                dom.div("Here is history data",id="history_content",cls="flex flex-col")

            with dom.form(UPLOAD_FORM_ATTRIS) as UploadForm:
                # 输入水印文字区
                with dom.div(cls=CARD1) as Card1:
                    dom.p("Write down your mark here",cls="text-base font-thin text-white" )
                    dom.input(cls=TEXT_INPUT,id="wm_text",type="text",name="mark_text",placeholder="your watermark text")
                # 上传图片区
                with dom.div(cls=CARD2) as Card2:
                    with dom.div(cls=DASHED_BOX):
                        dom.i(cls=UPLOAD_ICON,onclick='''$('#fileupload').click()''')
                        dom.p("Find File", id="show_info", cls="text-gray-500 mt-4")
                        dom.button("Upload", cls=UPLOAD_BUTTON,type="submit")
                        dom.input(cls="hidden", type="file", id="fileupload",name="ori_img",
                                  onchange='''$('#show_info').text(this.value.split("\\\\").pop(-1))''')

            # 生成水印图片区
            with dom.div(cls=RESULT_CONTAINER) as ResultContainer:
                dom.span(id="result_item")

    return ("{% load static %}"
            f"{doc.render()}")


def item(filename='{{filename}}'):
    with dom.div(cls=RESULT_ITEM) as ResultItem:
        dom.p(f'{filename}.jpg',cls="text-sm font-thin text-gray-400")
        with dom.a(href=f"/download?filename={filename}"):
            dom.i(cls="fas fa-download text-gray-300 font-medium text-base")
    return dom.span(id="result_item").render() + ResultItem.render()

def history_list(filename_list="{{ filename_list }}"):
    with dom.div(cls=HISTORY_ITEM) as HistoryItem:
        dom.p('{{filename}}.jpg',cls="text-base font-normal text-gray-800")
        with dom.a(href="/download?filename={{filename}}"):
            dom.i(cls="fas fa-download text-gray-800 font-medium text-lg")
    return (
        "{% for filename in filename_list %}"
            f"{HistoryItem.render()}"
        "{% endfor %}"
    )
    # 下面这么写返回也可以
    # return "{% for filename in filename_list %}" + \
    #        f"{HistoryItem.render()}" + "{% endfor %}"


with open('templates/page.html','w+') as f:
    f.write(page())

with open('templates/item.html','w+') as f:
    f.write(item())

with open('templates/history_list.html', 'w+') as f:
    f.write(history_list())