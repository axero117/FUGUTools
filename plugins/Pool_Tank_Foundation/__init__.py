"""水池计算插件。"""

from plugins.base_plugin import BasePlugin
from plugins.Pool_Tank_Foundation.widget import PoolTankFoundationWidget


class PoolTankFoundationPlugin(BasePlugin):
    """水池计算插件。"""

    def __init__(self):
        super().__init__()
        self._widget = None

    def get_name(self) -> str:
        """插件名称（显示在侧边栏）。"""
        return "水池计算"

    def get_description(self) -> str:
        """插件描述。"""
        return "计算水池基础混凝土/平衡层/换填材料用量，并进行多工况抗浮验算"

    def get_widget(self):
        """返回插件UI实例。"""
        if self._widget is None:
            self._widget = PoolTankFoundationWidget()
        return self._widget

    def on_load(self):
        """插件加载时回调。"""
        pass

    def on_unload(self):
        """插件卸载时回调。"""
        if self._widget:
            self._widget.deleteLater()
            self._widget = None
