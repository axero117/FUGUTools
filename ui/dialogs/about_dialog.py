"""关于对话框"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class AboutDialog(QDialog):
    """关于对话框"""
    
    def __init__(self, parent=None):
        """初始化关于对话框"""
        super().__init__(parent)
        
        # 设置对话框属性
        self.setWindowTitle("关于符构工具箱")
        self.setFixedSize(500, 700)
        self.setModal(True)
        
        # 初始化UI
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("符构工具箱 — 石化结构设计工具箱")
        title_font = QFont("Microsoft YaHei UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 版本
        version_label = QLabel("版本：v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)
        
        main_layout.addSpacing(20)
        
        # 创建文本浏览器，用于显示关于内容
        self._text_browser = QTextBrowser()
        self._text_browser.setOpenExternalLinks(True)
        self._text_browser.setReadOnly(True)
        
        # 设置内容
        self._set_about_content()
        
        main_layout.addWidget(self._text_browser)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.setFixedWidth(100)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
    
    def _set_about_content(self):
        """设置关于内容"""
        content = """
© 2026 刘佳龙（个人开发者）<br>
邮箱：<a href="mailto:axero117@outlook.com">axero117@outlook.com</a><br>
<br>
本工具为个人开发的免费工程辅助软件，<br>
旨在为石化行业结构设计人员提供便捷计算支持。<br>
<br>
──────────────────────────────<br>
<br>
<b>【开源软件声明】</b><br>
<br>
本软件使用了以下开源项目，特此致谢：<br>
<br>
• Python（ <a href="https://www.python.org/">https://www.python.org/</a> ）<br>
  许可证：Python Software Foundation License<br>
• PySide6 / Qt（ <a href="https://www.qt.io/qt-for-python">https://www.qt.io/qt-for-python</a> ）<br>
  许可证：GNU LGPL v3.0<br>
• loguru（ <a href="https://github.com/Delgan/loguru">https://github.com/Delgan/loguru</a> ）<br>
  许可证：MIT License<br>
<br>
完整许可证文本请见安装目录下的 LICENSES.txt 文件。<br>
<br>
──────────────────────────────<br>
<br>
<b>【使用说明】</b><br>
<br>
- 本软件主体代码由刘佳龙独立开发，保留所有权利。<br>
- 开源组件均按其原始许可证条款使用。<br>
- 若您对软件有建议或发现 Bug，欢迎邮件联系！<br>
<br>
感谢您的使用！
        """
        
        self._text_browser.setHtml(content)
