import hashlib

def set_md5(value,salt):
    """
    md5加密方式
    :param value:  加密数据
    :param salt:    加盐
    :return:
    """

    md5_str = hashlib.md5(salt.encode('utf-8'))
    md5_str.update(value.encode('utf-8'))
    return md5_str.hexdigest()