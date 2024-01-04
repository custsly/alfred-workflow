import base64
import time
from io import BytesIO

from PIL import ImageGrab, Image

from wf_utils import workflow_util
from ualfred import Workflow3


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
        return 'data:image/jpeg;base64,' + str(base64.b64encode(image_bytes), 'utf-8')


def build_md_image_without_var(image_name, image_base64):
    """
    构建 markdown 图标标签,
    不使用变量
    :param image_name: 图片名称
    :param image_base64: base64 编码
    :return:
    """
    return '![{0}]({1})'.format(image_name, image_base64)


def build_md_image_with_var(image_name, image_base64):
    """
    构建 markdown 图标标签,
    创建一个变量, 变量名为图片名称, 变量值为图片的 base64 编码
    通过变量引入图片, 中间是换行
    :param image_name: 图片名称
    :param image_base64: base64 编码
    :return:
    """
    image_base64_var = r'[{0}]: {1}'.format(image_name, image_base64)
    image_with_var = '![{0}][{1}]'.format(image_name, image_name)
    return image_with_var + '\n\n' + image_base64_var


def main():
    # workflow
    wf = Workflow3()
    img_base64 = image_bytes_base64_encode(read_clipboard_image())
    if not img_base64:
        workflow_util.add_wf_item(wf, title='not image in clipboard', subtitle=None, arg=None)
    else:
        image_name = 'clipboard_%s' % time.strftime("%Y%m%d%H%M%S", time.localtime())

        md_image_with_var = build_md_image_with_var(image_name, img_base64)
        md_image_without_var = build_md_image_without_var(image_name, img_base64)

        # 使用变量插入图片
        workflow_util.add_wf_item(wf, title=image_name,
                                  subtitle='md base64 image use var, length %s' % len(md_image_with_var),
                                  arg=md_image_with_var)
        # 不使用变量插入图片
        workflow_util.add_wf_item(wf, title=image_name,
                                  subtitle='md base64 image not var, length %s' % len(md_image_without_var),
                                  arg=md_image_without_var)
        # 仅有图片的base64字符串
        workflow_util.add_wf_item(wf, title=image_name, subtitle='only image base64, length %s' % len(img_base64),
                                  arg=img_base64)

    wf.send_feedback()


if __name__ == '__main__':
    main()
