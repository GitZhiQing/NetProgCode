import datetime
import mimetypes


def get_content_type(file_path):
    """
    根据文件路径获取文件的 MIME 类型
    """
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def get_gmt_date():
    """
    获取当前时间的 GMT 格式
    """
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
