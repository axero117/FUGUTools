"""型钢特性表插件"""

from plugins.base_plugin import BasePlugin
from plugins.Steel_Shape_Table.widget import SteelShapeTableWidget


class SteelShapeTablePlugin(BasePlugin):
    """型钢特性表插件"""
    
    def get_name(self) -> str:
        """获取插件名称
        
        Returns:
            插件名称
        """
        return "型钢特性表"
    
    def get_description(self) -> str:
        """获取插件描述
        
        Returns:
            插件描述
        """
        return "提供各种型钢的截面特性查询"
    
    def get_widget(self):
        """获取插件UI组件
        
        Returns:
            QWidget实例
        """
        return SteelShapeTableWidget()