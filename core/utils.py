"""通用工具函数模块"""

import os
import sys
import hashlib
import time
from pathlib import Path


def get_resource_path(relative_path: str) -> str:
    """获取资源文件的绝对路径
    
    Args:
        relative_path: 资源文件的相对路径
        
    Returns:
        资源文件的绝对路径
    """
    # 获取当前脚本所在目录
    base_path = Path(__file__).parent.parent
    return str(base_path / relative_path)


def calculate_file_hash(file_path: str, hash_algorithm: str = "md5") -> str:
    """计算文件哈希值
    
    Args:
        file_path: 文件路径
        hash_algorithm: 哈希算法，如 md5, sha1, sha256
        
    Returns:
        文件哈希值
    """
    hash_func = getattr(hashlib, hash_algorithm)
    h = hash_func()
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    
    return h.hexdigest()


def format_file_size(size_in_bytes: int) -> str:
    """格式化文件大小
    
    Args:
        size_in_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    
    return f"{size_in_bytes:.2f} PB"


def get_current_timestamp(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间戳
    
    Args:
        format_str: 时间格式字符串
        
    Returns:
        格式化后的时间字符串
    """
    return time.strftime(format_str, time.localtime())


def is_windows() -> bool:
    """检查是否为Windows系统
    
    Returns:
        是否为Windows系统
    """
    return sys.platform == "win32"


def is_macos() -> bool:
    """检查是否为macOS系统
    
    Returns:
        是否为macOS系统
    """
    return sys.platform == "darwin"


def is_linux() -> bool:
    """检查是否为Linux系统
    
    Returns:
        是否为Linux系统
    """
    return sys.platform.startswith("linux")


def create_dir_if_not_exists(dir_path: str):
    """创建目录（如果不存在）
    
    Args:
        dir_path: 目录路径
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def list_files(directory: str, extension: str = None) -> list:
    """列出目录中的文件
    
    Args:
        directory: 目录路径
        extension: 文件扩展名（如 ".txt"），不指定则列出所有文件
        
    Returns:
        文件路径列表
    """
    file_list = []
    directory_path = Path(directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        return file_list
    
    for item in directory_path.iterdir():
        if item.is_file():
            if extension is None or item.suffix == extension:
                file_list.append(str(item))
    
    return file_list
