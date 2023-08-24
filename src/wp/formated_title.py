from datetime import datetime


def get_title(value):
    white_keys = [',', '.']

    try:
        _text = value.split('\n')[0]
    except:
        return 'Новость ' + datetime.now().strftime("%H:%M:%S")

    msg = ''
    for x in _text:
        if x.isdigit() or x.isalpha() or x in white_keys:
            msg += x
        else:
            if x == ' ':
                msg += x

    try:
        if '  ' in msg:
            msg = msg.replace('  ', ' ')
    except:
        pass

    msg = msg.strip()

    return msg
