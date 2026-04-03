# AGENTS.md - FugoTools

## Project Overview

FugoTools 是一个面向石化行业的土木工程设计辅助工具集，基于 Python 和 PySide6 开发。采用插件化架构，便于功能扩展。

## Build & Run Commands

```bash
# 激活虚拟环境 (Windows PowerShell)
.venv\Scripts\activate

# 运行应用
python main.py

# 使用 PyInstaller 打包为 EXE
python build_exe.py

# 安装依赖
pip install -r requirements.txt
```

## Testing

当前尚未实现测试。添加测试时：

```bash
# 运行所有测试 (推荐 pytest)
pytest tests/

# 运行单个测试文件
pytest tests/test_module.py

# 运行单个测试函数
pytest tests/test_module.py::test_function_name
```

## Project Structure

```
FugoTools/
├── core/              # 核心模块 (app, config, logger, plugin_manager, utils)
├── plugins/           # 插件目录 (每个插件为独立子目录)
│   ├── base_plugin.py # 插件抽象基类
│   └── [PluginName]/  # 单个插件目录
│       ├── __init__.py    # 插件类定义 (继承 BasePlugin)
│       ├── widget.py      # UI 组件 (QWidget 子类)
│       └── logic.py       # 业务逻辑 (纯 Python，无 UI 依赖)
├── ui/                # UI 组件 (main_window, dialogs/, widgets/)
├── resources/         # 静态资源 (icons/, styles.qss)
├── config/            # 配置文件
├── tests/             # 测试目录 (当前为空)
├── build_exe.py       # PyInstaller 打包脚本
└── main.py            # 应用入口
```

## Code Style Guidelines

### 导入顺序

按以下顺序分组导入，组间空一行：

```python
# 标准库
import sys
import os
from pathlib import Path
import math
import json

# 第三方库
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QAction, QDoubleValidator

# 本地模块
from core.logger import Logger
from plugins.base_plugin import BasePlugin
```

### 命名约定

| 类型 | 风格 | 示例 |
|------|------|------|
| 类名 | PascalCase | `BasicBlockWidget`, `PluginManager` |
| 方法/函数 | snake_case | `get_name()`, `calculate_volume()` |
| 私有成员 | 前导下划线 | `_init_ui()`, `_logic`, `_connect_signals()` |
| 常量 | UPPER_SNAKE_CASE | `MAX_ITERATIONS` |
| 模块名 | 小写 snake_case | `plugin_manager.py`, `logic.py` |
| UI 控件 | 描述性名称 + 用途后缀 | `_length_input`, `_calculate_btn`, `_result_text` |

### 文档字符串

使用 Google 风格的中文 docstrings：

```python
def calculate_volume(length: float, width: float, height: float) -> float:
    """计算基础体积。

    Args:
        length: 基础长度 (m)
        width: 基础宽度 (m)
        height: 基础高度 (m)

    Returns:
        体积 (m³)
    """
    return length * width * height
```

### 类型提示

- 函数参数和返回值必须使用类型提示
- 可空类型使用 `Optional`
- 集合类型使用 `typing` 模块的 `List`, `Dict`, `Tuple`

```python
from typing import List, Optional, Dict, Tuple

def get_items(keyword: Optional[str] = None) -> List[str]:
    ...

def check_bearing_capacity(load: float, area: float) -> Tuple[bool, float]:
    ...
```

### 错误处理

- 文件 I/O 和外部操作使用 try-except
- 使用 Logger 类记录错误
- 错误信息使用中文

```python
from core.logger import Logger

logger = Logger()

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error(f"文件不存在: {file_path}")
except Exception as e:
    logger.error(f"加载文件失败: {e}")
```

### PySide6 GUI 约定

- Widget 类继承自 QWidget 或 QMainWindow
- 使用 Signal/Slot 机制，事件处理函数使用 `@Slot()` 装饰器
- 私有 UI 初始化方法：`_init_ui()`, `_connect_signals()`
- 输入验证使用 QDoubleValidator / QIntValidator
- 使用 `setProperty()` 添加自定义样式钩子

```python
class MyWidget(QWidget):
    # 定义信号
    calculation_done = Signal(float)

    def __init__(self):
        super().__init__()
        self._logic = MyLogic()  # 逻辑与 UI 分离
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self._input = QLineEdit()
        self._input.setValidator(QDoubleValidator(0.0, 1e9, 6))
        
        self._btn = QPushButton("计算")
        self._btn.setProperty("moduleAction", "primary")  # 样式钩子

    def _connect_signals(self):
        self._btn.clicked.connect(self._on_calculate)

    @Slot()
    def _on_calculate(self):
        result = self._logic.compute(float(self._input.text()))
        self.calculation_done.emit(result)
```

### 插件开发模式

**目录结构：**
```
plugins/[PluginName]/
├── __init__.py   # 插件类定义
├── widget.py     # UI 组件
└── logic.py      # 业务逻辑
```

**`__init__.py` 必须实现：**
```python
from plugins.base_plugin import BasePlugin
from plugins.PluginName.widget import PluginWidget

class PluginNamePlugin(BasePlugin):
    def get_name(self) -> str:
        return "插件显示名称"
    
    def get_description(self) -> str:
        return "插件功能描述"
    
    def get_widget(self):
        if self._widget is None:
            self._widget = PluginWidget()
        return self._widget
    
    def on_load(self):
        pass  # 可选：初始化资源
    
    def on_unload(self):
        if self._widget:
            self._widget.deleteLater()
            self._widget = None
```

**Widget 推荐实现的方法：**
| 方法 | 用途 |
|------|------|
| `reset()` | 重置 UI 到初始状态 |
| `save(file_path)` | 保存参数到文件 |
| `open(file_path)` | 从文件加载参数 |

**Logic 类规范：**
- 纯 Python 类，不依赖 PySide6
- 每个方法对应一个独立计算
- 完整的 docstrings 说明参数单位和返回值

## 配置

- 应用配置：`core/config.py`
- 日志系统：`core/logger.py` (Python logging 模块)
- 样式表：`resources/styles.qss` (Qt Stylesheets)

## 依赖

- Python 3.8+
- PySide6 6.4.3
- PyYAML, pandas, plotly, openpyxl, xlrd, python-docx
- PyInstaller (打包 EXE)

## 交互要求

请始终使用简体中文进行回复，除非我明确要求使用其他语言。涉及编程术语时，请保留英文原文并（在必要时）提供中文解释。