"""YJK柱脚内力处理工具插件"""

from plugins.base_plugin import BasePlugin
from plugins.YJK_Column_Force.widget import YJKColumnForceWidget


class YJKColumnForcePlugin(BasePlugin):
    """YJK柱脚内力处理工具插件"""
    
    def __init__(self):
        """初始化插件"""
        super().__init__()
        self._widget = None
    
    def get_name(self) -> str:
        """获取插件名称"""
        return "YJK柱脚内力处理工具"
    
    def get_description(self) -> str:
        """获取插件描述"""
        return "处理YJK柱脚内力数据，支持导出压力、拉力和全部内力数据"
    
    def get_widget(self):
        """获取插件UI组件"""
        if self._widget is None:
            self._widget = YJKColumnForceWidget()
        return self._widget
    
    def on_load(self):
        """插件加载时调用"""
        pass
    
    def on_unload(self):
        """插件卸载时调用"""
        if self._widget:
            self._widget.deleteLater()
            self._widget = None
