"""插件抽象基类"""

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """插件抽象基类"""
    
    @abstractmethod
    def get_name(self) -> str:
        """获取插件名称
        
        Returns:
            插件名称
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取插件描述
        
        Returns:
            插件描述
        """
        pass
    
    @abstractmethod
    def get_widget(self):
        """获取插件UI组件
        
        Returns:
            QWidget实例
        """
        pass
    
    def on_load(self):
        """插件加载时调用
        
        可用于初始化资源、连接信号等
        """
        pass
    
    def on_unload(self):
        """插件卸载时调用
        
        可用于清理资源、断开信号等
        """
        pass
