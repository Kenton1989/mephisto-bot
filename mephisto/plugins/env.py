import os

def _load_su():
    su_str = os.environ.get('QQ_BOT_SU', '')

    su_list = su_str.split(":")

    if len(su_list) == 1 and su_list[0] == "":
        return {}
    
    return set(int(uid) for uid in su_list)

SUPERUSER = _load_su()


