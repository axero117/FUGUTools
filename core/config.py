"""配置管理模块"""

import json
import yaml
import os
from pathlib import Path


class Config:
    """配置管理类，支持JSON和YAML格式"""
    
    def __init__(self, config_dir: str = "config"):
        """初始化配置管理器
        
        Args:
            config_dir: 配置文件目录
        """
        self._config_dir = Path(config_dir)
        self._config_dir.mkdir(exist_ok=True)
        
        self._config = {}
        self._load_default_config()
    
    def _load_default_config(self):
        """加载默认配置"""
        self._config = {
            "app": {
                "language": "zh_CN",
                "window_size": [1024, 768],
                "window_position": [100, 100]
            },
            "logger": {
                "level": "INFO",
                "file": "logs/fugo_toolbox.log",
                "max_bytes": 10485760,
                "backup_count": 5
            },
            "plugins": {
                "enabled": [],
                "disabled": []
            }
        }
    
    def load(self, config_file: str):
        """加载配置文件
        
        Args:
            config_file: 配置文件路径
        """
        config_path = Path(config_file)
        if not config_path.exists():
            self.save(config_file)
            return
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                if config_path.suffix == ".json":
                    loaded_config = json.load(f)
                elif config_path.suffix in [".yaml", ".yml"]:
                    loaded_config = yaml.safe_load(f)
                else:
                    raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")
            
            # 合并配置
            self._merge_configs(self._config, loaded_config)
        except Exception as e:
            print(f"Failed to load config: {e}")
    
    def save(self, config_file: str):
        """保存配置到文件
        
        Args:
            config_file: 配置文件路径
        """
        config_path = Path(config_file)
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                if config_path.suffix == ".json":
                    json.dump(self._config, f, indent=2, ensure_ascii=False)
                elif config_path.suffix in [".yaml", ".yml"]:
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path.suffix}")
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def get(self, key: str, default=None):
        """获取配置值
        
        Args:
            key: 配置键，支持点分隔符（如 "app.theme"）
            default: 默认值
        
        Returns:
            配置值
        """
        keys = key.split(".")
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value):
        """设置配置值
        
        Args:
            key: 配置键，支持点分隔符（如 "app.theme"）
            value: 配置值
        """
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    @staticmethod
    def _merge_configs(base, override):
        """合并配置
        
        Args:
            base: 基础配置
            override: 覆盖配置
        """
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                Config._merge_configs(base[key], value)
            else:
                base[key] = value
