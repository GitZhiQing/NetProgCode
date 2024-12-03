import datetime
import mimetypes

import magic  # python-magic-bin


def get_content_type_by_file_path(file_path):
    """
    根据文件路径获取文件的 MIME 类型
    """
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def get_content_type_by_content(content):
    """
    根据文件内容获取文件的 MIME 类型
    """
    try:
        return magic.Magic(mime=True).from_buffer(content)
    except ImportError:
        return "application/octet-stream"


def get_gmt_date():
    """
    获取当前时间的 GMT 格式
    """
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
