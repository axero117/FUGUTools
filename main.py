#!/usr/bin/env python3
"""FugoToolbox 主入口脚本"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.app import FugoApp


def main():
    """主函数"""
    app = FugoApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
