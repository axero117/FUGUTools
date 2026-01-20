"""QApplication 封装"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from core.config import Config
from core.logger import Logger
from core.plugin_manager import PluginManager
from ui.main_window import MainWindow


class FugoApp:
    """FugoToolbox 应用程序类"""
    
    def __init__(self):
        """初始化应用程序"""
        self._app = QApplication(sys.argv)
        self._app.setApplicationName("FugoToolbox")
        self._app.setApplicationVersion("1.0.0")
        
        # 初始化核心组件
        self._config = Config()
        self._logger = Logger()
        self._plugin_manager = PluginManager()
        
        # 初始化主窗口
        self._main_window = MainWindow()
        
    def run(self):
        """运行应用程序"""
        # 第一阶段：加载插件（仅发现和注册，不实例化）
        self._plugin_manager.load_plugins()
        
        # 将插件信息注册到主窗口，但不立即实例化
        plugin_registry = self._plugin_manager.get_plugin_registry()
        for plugin_info in plugin_registry:
            plugin_name = plugin_info["name"]
            self._main_window.register_plugin(plugin_name)
        
        # 显示主窗口
        self._main_window.show()
        
        # 设置主窗口的应用实例引用和插件管理器引用
        self._main_window.set_app_instance(self)
        self._main_window.set_plugin_manager(self._plugin_manager)
        
        # 应用样式
        self._apply_stylesheet()
        
        # 运行事件循环
        return self._app.exec()
    
    def _apply_stylesheet(self):
        """应用全局样式表"""
        try:
            # 直接加载白天模式样式表
            stylesheet_path = "resources/styles.qss"
            
            with open(stylesheet_path, "r", encoding="utf-8") as f:
                self._app.setStyleSheet(f.read())
            
            self._logger.info("Applied light theme")
        except Exception as e:
            self._logger.error(f"加载样式表失败: {e}")
