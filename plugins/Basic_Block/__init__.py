"""块式基础计算插件"""

from plugins.base_plugin import BasePlugin
from plugins.Basic_Block.widget import BasicBlockWidget


class BasicBlockPlugin(BasePlugin):
    """块式基础计算插件"""
    
    def __init__(self):
        """初始化插件"""
        super().__init__()
        self._widget = None
    
    def get_name(self) -> str:
        """获取插件名称"""
        return "块式基础计算"
    
    def get_description(self) -> str:
        """获取插件描述"""
        return "提供基础的块式计算功能"
    
    def get_widget(self):
        """获取插件UI组件"""
        if self._widget is None:
            self._widget = BasicBlockWidget()
        return self._widget
    
    def on_load(self):
        """插件加载时调用"""
        pass
    
    def on_unload(self):
        """插件卸载时调用"""
        if self._widget:
            self._widget.deleteLater()
            self._widget = None
