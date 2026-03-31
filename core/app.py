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
        self._app.setApplicationVersion("1.0.1")
        
        # 初始化核心组件
        self._config = Config()
        self._logger = Logger()
        self._plugin_manager = PluginManager()
        
        # 初始化主窗口
        self._main_window = MainWindow()
        
        # 设置应用程序图标
        self._set_app_icon()
        
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
    
    def _set_app_icon(self):
        """设置应用程序图标"""
        try:
            # 处理PyInstaller打包后的路径问题
            import sys
            from pathlib import Path
            
            if hasattr(sys, '_MEIPASS'):
                # 打包后的临时提取目录
                base_path = Path(sys._MEIPASS)
            else:
                # 开发环境下的项目根目录
                base_path = Path(__file__).parent.parent
            
            # 加载应用图标
            icon_path = base_path / "resources" / "icons" / "favicon (1).ico"
            
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self._app.setWindowIcon(icon)
                self._main_window.setWindowIcon(icon)
                self._logger.info(f"设置应用图标: {icon_path}")
            else:
                self._logger.warning(f"图标文件不存在: {icon_path}")
        except Exception as e:
            self._logger.error(f"设置应用图标失败: {e}")

    def _apply_stylesheet(self):
        """应用全局样式表"""
        try:
            # 处理PyInstaller打包后的路径问题
            import sys
            from pathlib import Path
            
            if hasattr(sys, '_MEIPASS'):
                # 打包后的临时提取目录
                base_path = Path(sys._MEIPASS)
            else:
                # 开发环境下的项目根目录
                base_path = Path(__file__).parent.parent
            
            # 加载白天模式样式表
            stylesheet_path = base_path / "resources" / "styles.qss"
            
            with open(stylesheet_path, "r", encoding="utf-8") as f:
                self._app.setStyleSheet(f.read())
            
            self._logger.info("Applied light theme")
        except Exception as e:
            self._logger.error(f"加载样式表失败: {e}")
