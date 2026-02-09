"""日志系统模块"""

import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path


class Logger:
    """日志管理类"""
    
    def __init__(self):
        """初始化日志系统"""
        self._logger = logging.getLogger("FugoToolbox")
        self._logger.setLevel(logging.DEBUG)
        
        # 清除已存在的处理器
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
        
        # 配置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        
        # 只添加控制台处理器，不添加文件处理器，避免创建logs目录
        self._logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """记录调试信息
        
        Args:
            message: 日志信息
        """
        self._logger.debug(message)
    
    def info(self, message: str):
        """记录普通信息
        
        Args:
            message: 日志信息
        """
        self._logger.info(message)
    
    def warning(self, message: str):
        """记录警告信息
        
        Args:
            message: 日志信息
        """
        self._logger.warning(message)
    
    def error(self, message: str):
        """记录错误信息
        
        Args:
            message: 日志信息
        """
        self._logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误信息
        
        Args:
            message: 日志信息
        """
        self._logger.critical(message)
    
    def exception(self, message: str):
        """记录异常信息
        
        Args:
            message: 日志信息
        """
        self._logger.exception(message)
