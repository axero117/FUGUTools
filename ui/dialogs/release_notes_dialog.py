from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QFrame
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
import os

class ReleaseNotesDialog(QDialog):
    """更新说明对话框"""
    
    def __init__(self, parent=None):
        """初始化更新说明对话框"""
        super().__init__(parent)
        
        # 设置对话框属性
        self.setWindowTitle("更新说明")
        self.setFixedSize(600, 500)
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
        title_label = QLabel("符构工具箱 - 更新说明")
        title_font = QFont("Microsoft YaHei UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # 加载更新说明文本
        notes_text = QTextBrowser()
        notes_text.setOpenExternalLinks(True)  # 允许打开外部链接
        
        # 尝试读取项目根目录下的 ReleaseNotes.md 文件
        try:
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建 ReleaseNotes.md 的路径（相对于当前文件）
            notes_path = os.path.join(current_dir, "..", "..", "ReleaseNotes.md")
            
            with open(notes_path, 'r', encoding='utf-8') as f:
                content = f.read()
                notes_text.setMarkdown(content)
        except Exception as e:
            notes_text.setText(f"无法加载更新说明文件: {str(e)}")
        
        main_layout.addWidget(notes_text, 1)  # 添加拉伸因子，占据剩余空间
        
        # 确认按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
        
        # 设置窗口图标（可选，与主窗口一致）
        self.setWindowIcon(QIcon(":/icons/logo.png"))  # 假设有一个logo图标，如果路径不对可以移除或调整