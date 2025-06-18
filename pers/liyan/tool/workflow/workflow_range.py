# -*- coding: UTF-8 -*-

import sys
from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args, clip_content):
    """
    Generate number sequence, parameter format: start,end
    :param args: command line arguments, start,end
    :param clip_content:
    :return:
    """
    # workflow
    wf = Workflow3()

    # Parameter validation, format should be start,end
    if len(args) <= 1:
        workflow_util.add_wf_item(wf,
                                  title='Parameter Error',
                                  subtitle='Format should be: start,end',
                                  arg='Parameter Error')
        wf.send_feedback()
        return

    try:
        # Parse parameters
        param = args[1]
        start_end = param.split(',')
        if len(start_end) != 2:
            raise ValueError()

        start = int(start_end[0])
        end = int(start_end[1])

        # Determine zero-padding length
        max_num = max(abs(start), abs(end))
        padding_length = len(str(max_num))

        # Generate both variants of the sequence
        # Default: include both start and end
        step = 1 if start <= end else -1
        numbers_inclusive = range(start, end + step, step)

        # Option key: include start but exclude end
        numbers_exclusive = range(start, end, step)

        # Generate various formats for both variants
        # Inclusive formats
        padded_numbers_inc = [str(num).zfill(padding_length) for num in numbers_inclusive]
        plain_numbers_inc = [str(num) for num in numbers_inclusive]

        # Exclusive formats
        padded_numbers_exc = [str(num).zfill(padding_length) for num in numbers_exclusive]
        plain_numbers_exc = [str(num) for num in numbers_exclusive]

        # Convert to different delimiter formats
        # Newline separated
        padded_lines_inc = '\n'.join(padded_numbers_inc)
        plain_lines_inc = '\n'.join(plain_numbers_inc)
        padded_lines_exc = '\n'.join(padded_numbers_exc)
        plain_lines_exc = '\n'.join(plain_numbers_exc)

        # Comma separated
        padded_comma_inc = ', '.join(padded_numbers_inc)
        plain_comma_inc = ', '.join(plain_numbers_inc)
        padded_comma_exc = ', '.join(padded_numbers_exc)
        plain_comma_exc = ', '.join(plain_numbers_exc)

        # Tab separated
        padded_tab_inc = '\t'.join(padded_numbers_inc)
        plain_tab_inc = '\t'.join(plain_numbers_inc)
        padded_tab_exc = '\t'.join(padded_numbers_exc)
        plain_tab_exc = '\t'.join(plain_numbers_exc)

        # Add options to workflow with modifiers

        # Zero-padded formats
        item = workflow_util.add_wf_item(wf,
                                         title='Zero-padded - Newline separated',
                                         subtitle=f'From {start} to {end} (both included)',
                                         arg=padded_lines_inc)
        item.add_modifier('alt',
                          subtitle=f'From {start} (included) to {end} (excluded)',
                          arg=padded_lines_exc)

        item = workflow_util.add_wf_item(wf,
                                         title='Zero-padded - Comma separated',
                                         subtitle=f'From {start} to {end} (both included)',
                                         arg=padded_comma_inc)
        item.add_modifier('alt',
                          subtitle=f'From {start} (included) to {end} (excluded)',
                          arg=padded_comma_exc)

        item = workflow_util.add_wf_item(wf,
                                         title='Zero-padded - Tab separated',
                                         subtitle=f'From {start} to {end} (both included)',
                                         arg=padded_tab_inc)
        item.add_modifier('alt',
                          subtitle=f'From {start} (included) to {end} (excluded)',
                          arg=padded_tab_exc)

        # Plain formats
        item = workflow_util.add_wf_item(wf,
                                         title='Plain numbers - Newline separated',
                                         subtitle=f'From {start} to {end} (both included)',
                                         arg=plain_lines_inc)
        item.add_modifier('alt',
                          subtitle=f'From {start} (included) to {end} (excluded)',
                          arg=plain_lines_exc)

        item = workflow_util.add_wf_item(wf,
                                         title='Plain numbers - Comma separated',
                                         subtitle=f'From {start} to {end} (both included)',
                                         arg=plain_comma_inc)
        item.add_modifier('alt',
                          subtitle=f'From {start} (included) to {end} (excluded)',
                          arg=plain_comma_exc)

        item = workflow_util.add_wf_item(wf,
                                         title='Plain numbers - Tab separated',
                                         subtitle=f'From {start} to {end} (both included)',
                                         arg=plain_tab_inc)
        item.add_modifier('alt',
                          subtitle=f'From {start} (included) to {end} (excluded)',
                          arg=plain_tab_exc)

    except ValueError:
        workflow_util.add_wf_item(wf,
                                  title='Parameter Error',
                                  subtitle='Should be integers, format: start,end',
                                  arg='Parameter Error')

    wf.send_feedback()


def main():
    flow(sys.argv, None)


if __name__ == '__main__':
    main()
