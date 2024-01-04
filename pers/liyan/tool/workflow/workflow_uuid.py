# -*- coding: UTF-8 -*-

import uuid
import sys
from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args, clip_content):
    """
    生成给定数量的uuid
    :param args: 命令行参数, 数量
    :param clip_content:
    :return:
    """
    count = 1
    if len(args) > 1 and args[1]:
        try:
            arg_count = int(args[1])
            if arg_count > 1:
                count = arg_count
        except ValueError as e:
            pass

    uuid_list = [str(uuid.uuid1()) for i in range(1, count + 1)]

    # workflow
    wf = Workflow3()

    # 不做处理
    uuid_lines = '\n'.join(uuid_list)
    workflow_util.add_wf_item(wf, title='original uuid', subtitle='%s...' % uuid_list[0], arg=uuid_lines)

    # 去掉 -
    simple_uuid_list = list(map(lambda x: x.replace('-', ''), uuid_list))
    simple_uuid_lines = '\n'.join(simple_uuid_list)
    workflow_util.add_wf_item(wf, title='uuid remove -', subtitle='%s...' % simple_uuid_list[0], arg=simple_uuid_lines)

    # 大写
    upper_uuid_list = list(map(lambda x: x.upper(), uuid_list))
    upper_uuid_lines = '\n'.join(upper_uuid_list)
    workflow_util.add_wf_item(wf, title='uuid upper case', subtitle='%s...' % upper_uuid_list[0], arg=upper_uuid_lines)

    # 大写去掉 -
    upper_simple_uuid_list = list(map(lambda x: x.replace('-', '').upper(), uuid_list))
    upper_simple_uuid_lines = '\n'.join(upper_simple_uuid_list)
    workflow_util.add_wf_item(wf, title='uuid upper case remove -', subtitle='%s...' % upper_simple_uuid_list[0],
                              arg=upper_simple_uuid_lines)

    wf.send_feedback()


def main():
    flow(sys.argv, None)


if __name__ == '__main__':
    main()
