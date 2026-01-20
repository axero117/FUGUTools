"""插件管理模块"""

import importlib
import os
import sys
from pathlib import Path

from core.logger import Logger
from plugins.base_plugin import BasePlugin


class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        """初始化插件管理器"""
        self._logger = Logger()
        self._plugins = []  # 已实例化的插件列表
        self._plugin_registry = []  # 插件注册表，存储插件类和元信息
        self._plugin_dirs = [Path("plugins")]
    
    def add_plugin_dir(self, plugin_dir: str):
        """添加插件目录
        
        Args:
            plugin_dir: 插件目录路径
        """
        plugin_path = Path(plugin_dir)
        if plugin_path.exists() and plugin_path not in self._plugin_dirs:
            self._plugin_dirs.append(plugin_path)
    
    def load_plugins(self):
        """第一阶段：发现和注册插件，不实例化
        
        扫描插件目录，发现并注册插件，但不实例化，只存储插件类和元信息
        """
        self._logger.info("Loading plugins (phase 1: discovery)...")
        
        for plugin_dir in self._plugin_dirs:
            self._discover_plugins_from_dir(plugin_dir)
        
        self._logger.info(f"Discovered {len(self._plugin_registry)} plugins")
    
    def _discover_plugins_from_dir(self, plugin_dir: Path):
        """从指定目录发现插件
        
        Args:
            plugin_dir: 插件目录路径
        """
        if not plugin_dir.exists():
            self._logger.warning(f"Plugin directory not found: {plugin_dir}")
            return
        
        # 遍历插件目录
        for item in plugin_dir.iterdir():
            if not item.is_dir():
                continue
            
            # 跳过__pycache__等目录
            if item.name.startswith("_"):
                continue
            
            # 检查是否有__init__.py文件
            init_file = item / "__init__.py"
            if not init_file.exists():
                self._logger.warning(f"Missing __init__.py in plugin: {item.name}")
                continue
            
            # 尝试导入插件
            try:
                # 添加插件目录到Python路径
                plugin_root = str(plugin_dir.parent)
                if plugin_root not in sys.path:
                    sys.path.insert(0, plugin_root)
                
                # 导入插件模块
                plugin_module_name = f"plugins.{item.name}"
                plugin_module = importlib.import_module(plugin_module_name)
                
                # 查找插件类
                plugin_class = None
                for attr_name in dir(plugin_module):
                    attr = getattr(plugin_module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr is not BasePlugin:
                        plugin_class = attr
                        break
                
                if not plugin_class:
                    self._logger.warning(f"No BasePlugin subclass found in {plugin_module_name}")
                    continue
                
                # 创建临时实例获取插件信息
                temp_instance = plugin_class()
                plugin_info = {
                    "name": temp_instance.get_name(),
                    "description": temp_instance.get_description(),
                    "plugin_class": plugin_class,
                    "module_name": plugin_module_name,
                    "plugin_dir": str(item)
                }
                del temp_instance  # 立即销毁临时实例
                
                # 将插件信息添加到注册表
                self._plugin_registry.append(plugin_info)
                self._logger.info(f"Discovered plugin: {plugin_info['name']}")
                
            except Exception as e:
                self._logger.error(f"发现插件 {item.name} 失败: {e}")
                import traceback
                traceback.print_exc()
    
    def instantiate_plugin(self, plugin_name: str):
        """第二阶段：实例化指定名称的插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            BasePlugin: 实例化的插件，已调用on_load()方法
            None: 如果插件未找到
        """
        # 检查插件是否已实例化
        for plugin in self._plugins:
            if plugin.get_name() == plugin_name:
                return plugin
        
        # 查找插件信息
        plugin_info = next((p for p in self._plugin_registry if p["name"] == plugin_name), None)
        if not plugin_info:
            self._logger.warning(f"Plugin not found in registry: {plugin_name}")
            return None
        
        # 实例化插件
        try:
            self._logger.info(f"Instantiating plugin: {plugin_name}")
            plugin = plugin_info["plugin_class"]()
            plugin.on_load()
            self._plugins.append(plugin)
            return plugin
        except Exception as e:
            self._logger.error(f"实例化插件 {plugin_name} 失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def instantiate_all_plugins(self):
        """第二阶段：实例化所有已发现的插件
        
        Returns:
            list: 所有实例化的插件列表
        """
        self._logger.info("Instantiating all plugins (phase 2: instantiation)...")
        
        for plugin_info in self._plugin_registry:
            if not any(p.get_name() == plugin_info["name"] for p in self._plugins):
                self.instantiate_plugin(plugin_info["name"])
        
        self._logger.info(f"Instantiated {len(self._plugins)} plugins")
        return self._plugins
    
    def get_plugins(self):
        """获取所有已实例化的插件
        
        Returns:
            list: 已实例化的插件列表
        """
        return self._plugins.copy()
    
    def get_plugin(self, name: str):
        """根据名称获取插件
        
        Args:
            name: 插件名称
            
        Returns:
            BasePlugin: 插件实例，若未找到则返回None
        """
        # 先检查已实例化的插件
        plugin = next((p for p in self._plugins if p.get_name() == name), None)
        if plugin:
            return plugin
        
        # 如果未实例化，则尝试实例化
        return self.instantiate_plugin(name)
    
    def get_plugin_registry(self):
        """获取插件注册表
        
        Returns:
            list: 插件注册表，包含插件名称、描述等元信息
        """
        return [{"name": p["name"], "description": p["description"]} for p in self._plugin_registry]
    
    def unload_plugins(self):
        """卸载所有插件
        
        调用每个插件的on_unload()方法，然后清空插件列表
        """
        for plugin in self._plugins:
            try:
                plugin.on_unload()
                self._logger.info(f"Unloaded plugin: {plugin.get_name()}")
            except Exception as e:
                self._logger.error(f"卸载插件 {plugin.get_name()} 失败: {e}")
                import traceback
                traceback.print_exc()
        
        self._plugins.clear()
    
    def unload_plugin(self, plugin_name: str):
        """卸载指定名称的插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 是否卸载成功
        """
        for plugin in self._plugins:
            if plugin.get_name() == plugin_name:
                try:
                    plugin.on_unload()
                    self._plugins.remove(plugin)
                    self._logger.info(f"Unloaded plugin: {plugin_name}")
                    return True
                except Exception as e:
                    self._logger.error(f"卸载插件 {plugin_name} 失败: {e}")
                    import traceback
                    traceback.print_exc()
        return False