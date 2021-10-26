import base64
import time
from io import BytesIO

from PIL import ImageGrab, Image

from wf_utils import workflow_util
from workflow import Workflow3


def read_clipboard_image():
    """
    获取剪贴板里的图片
    :return: byte[]
    """
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        temp_buffer = BytesIO()
        img.save(temp_buffer, format='JPEG')
        return temp_buffer.getvalue()
    else:
        return None


def image_bytes_base64_encode(image_bytes):
    """
    图片的 byte数组 编码为base64字符串
    :return: 编码后base64 字符串
    """
    if image_bytes is not None:
        return str(base64.b64encode(image_bytes), 'utf-8')


def build_md_image_tag(image_name, image_base64):
    """
    构建 markdown 图标标签,
    创建一个变量, 变量名为图片名称, 变量值为图片的 base64 编码, 不包括头的部分
    通过变量引入图片
    :param image_name: 图片名称
    :param image_base64: base64 编码
    :return:
    """
    full_image_base64 = 'data:image/jpeg;base64,' + image_base64
    image_base64_var = r'[{0}]: {1}'.format(image_name, full_image_base64)
    image_tag = '![{0}][{1}]'.format(image_name, image_name)
    return image_tag + '\n\n' + image_base64_var


def main():
    # workflow
    wf = Workflow3()
    img_base64 = image_bytes_base64_encode(read_clipboard_image())
    if not img_base64:
        workflow_util.add_wf_item(wf, title='not image in clipboard', subtitle=None, arg=None)
    else:
        image_name = 'clipboard_%s' % time.strftime("%Y%m%d%H%M%S", time.localtime())
        image_tag_str = build_md_image_tag(image_name, img_base64)
        workflow_util.add_wf_item(wf, title=image_name, subtitle='length %s' % len(image_tag_str), arg=image_tag_str)

    wf.send_feedback()


if __name__ == '__main__':
    main()
