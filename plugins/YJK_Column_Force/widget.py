"""YJK柱脚内力处理工具UI组件"""

import sys
import os
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QFrame, QTextEdit, QStyle, QDialog, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QTextCursor

from plugins.YJK_Column_Force.logic import YJKColumnForceLogic


class YJKColumnForceWidget(QWidget):
    """YJK柱脚内力处理工具UI组件"""
    
    def __init__(self):
        """初始化UI组件"""
        super().__init__()
        
        # 启用拖放功能
        self.setAcceptDrops(True)
        
        # 初始化业务逻辑
        self._logic = YJKColumnForceLogic()
        
        # 模式标志：当前是否显示原版界面
        self._current_mode = "original"  # "original" 或 "explorer"
        
        # 初始化UI
        self._init_ui()
        
        # 连接信号和槽
        self._connect_signals()

        # 设置鼠标事件透明，允许拖放事件穿透
        self.file_info_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.log_text.setAttribute(Qt.WA_TransparentForMouseEvents)
    
    def _init_ui(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(25)
        
        # 设置布局的拖放属性
        main_layout.setEnabled(True)

        # 模式切换区域
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(10)
        mode_layout.setAlignment(Qt.AlignLeft)
        
        # 原版模式按钮
        self.original_mode_btn = QPushButton("原版柱底力导出")
        self.original_mode_btn.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.original_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2c80b9;
            }
            QPushButton:pressed {
                background-color: #256d9c;
            }
            QPushButton:checked {
                background-color: #256d9c;
            }
        """)
        self.original_mode_btn.setCheckable(True)
        self.original_mode_btn.setChecked(True)
        mode_layout.addWidget(self.original_mode_btn)
        
        # 探索者模式按钮
        self.explorer_mode_btn = QPushButton("探索者柱底力导出")
        self.explorer_mode_btn.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.explorer_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2c80b9;
            }
            QPushButton:pressed {
                background-color: #256d9c;
            }
            QPushButton:checked {
                background-color: #256d9c;
            }
        """)
        self.explorer_mode_btn.setCheckable(True)
        mode_layout.addWidget(self.explorer_mode_btn)
        
        # 添加模式切换区域到主布局
        main_layout.addLayout(mode_layout)

        # 标题区域
        self.title_label = QLabel("YJK柱脚内力格式调整工具")
        self.title_label.setFont(QFont("微软雅黑", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        main_layout.addWidget(self.title_label)

        # 文件选择区域
        file_widget = QWidget()
        file_layout = QVBoxLayout(file_widget)
        file_layout.setSpacing(15)

        # 选择文件按钮
        self.select_btn = QPushButton("📁 选择YJK表格文件")
        self.select_btn.setFixedHeight(50)
        self.select_btn.setFont(QFont("微软雅黑", 12))
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 6px;
                padding: 12px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2c80b9;
            }
            QPushButton:pressed {
                background-color: #256d9c;
            }
        """)

        # 文件信息显示区域
        self.file_info_label = QLabel("未选择文件")
        self.file_info_label.setFont(QFont("微软雅黑", 10))
        self.file_info_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 15px;
                min-height: 70px;
                color: #495057;
            }
        """)
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setAlignment(Qt.AlignTop)

        file_layout.addWidget(self.select_btn)
        file_layout.addWidget(self.file_info_label)
        main_layout.addWidget(file_widget)

        # 功能按钮区域
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(15)

        # 按钮样式
        button_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 14px 20px;
                border-radius: 6px;
                margin: 5px 0;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """

        # 导出压力按钮
        self.export_pressure_btn = QPushButton("📤 导出全部压力数据")
        self.export_pressure_btn.setFixedHeight(60)
        self.export_pressure_btn.setFont(QFont("微软雅黑", 12))
        self.export_pressure_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2ecc71;
                color: white;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)
        self.export_pressure_btn.setEnabled(False)

        # 导出拉力按钮
        self.export_tension_btn = QPushButton("📤 导出全部拉力数据")
        self.export_tension_btn.setFixedHeight(60)
        self.export_tension_btn.setFont(QFont("微软雅黑", 12))
        self.export_tension_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.export_tension_btn.setEnabled(False)

        # 导出全部柱底内力按钮
        self.export_all_btn = QPushButton("📤 导出全部柱底内力")
        self.export_all_btn.setFixedHeight(60)
        self.export_all_btn.setFont(QFont("微软雅黑", 12))
        self.export_all_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #f39c12;
                color: white;
            }
            QPushButton:hover {
                background-color: #d68910;
            }
            QPushButton:pressed {
                background-color: #b9770e;
            }
        """)
        self.export_all_btn.setEnabled(False)

        buttons_layout.addWidget(self.export_pressure_btn)
        buttons_layout.addWidget(self.export_tension_btn)
        buttons_layout.addWidget(self.export_all_btn)
        main_layout.addWidget(buttons_widget)

        # 日志区域
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)

        log_label = QLabel("操作日志")
        log_label.setFont(QFont("微软雅黑", 11, QFont.Bold))
        log_label.setStyleSheet("color: #34495e; margin-bottom: 5px;")
        log_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(120)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
                color: #212529;
            }
        """)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)

        main_layout.addWidget(log_widget)

        # 文件路径
        self.file_path = ""
        
        # 在文件信息区域禁用拖放（由主widget处理）
        self.file_info_label.setAcceptDrops(False)  # 子控件不处理拖放
        self.select_btn.setAcceptDrops(False)
        
        # 在工作区设置拖放属性
        self.log_text.setAcceptDrops(False)
        
        # 启用整个widget的拖放
        self.setMouseTracking(True)

    def _connect_signals(self):
        """连接信号和槽"""
        # 按钮点击信号
        self.select_btn.clicked.connect(self.select_file)
        self.export_pressure_btn.clicked.connect(self.process_pressure)
        self.export_tension_btn.clicked.connect(self.process_tension)
        self.export_all_btn.clicked.connect(self.process_all)
        
        # 模式切换按钮信号
        self.original_mode_btn.clicked.connect(self._on_original_mode_clicked)
        self.explorer_mode_btn.clicked.connect(self._on_explorer_mode_clicked)

    def log_message(self, message, level="info"):
        """添加日志消息，支持不同级别"""
        timestamp = pd.Timestamp.now().strftime("%H:%M:%S")
        color = {
            "info": "#2c3e50",
            "success": "#27ae60",
            "warning": "#f39c12",
            "error": "#e74c3c"
        }.get(level, "#2c3e50")

        self.log_text.append(
            f'<span style="color:{color}">[{timestamp}] {message}</span>')
        # 滚动到底部
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)

    def set_file(self, file_path):
        """设置文件路径并更新UI"""
        if not file_path:
            return

        self.file_path = file_path
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # KB

        # 更新文件信息显示
        file_info = f"""
        <b>已选择文件:</b> {file_name}<br>
        <b>文件大小:</b> {file_size:.2f} KB<br>
        <b>文件类型:</b> Excel文件
        """
        self.file_info_label.setText(file_info)
        self.file_info_label.setStyleSheet("""
            QLabel {
                background-color: #e8f5e9;
                border: 1px solid #c8e6c9;
                border-radius: 6px;
                padding: 15px;
                min-height: 70px;
                color: #1b5e20;
            }
        """)

        # 启用处理按钮
        self.export_pressure_btn.setEnabled(True)
        self.export_tension_btn.setEnabled(True)
        self.export_all_btn.setEnabled(True)

        # 更新日志
        self.log_message(f"已选择文件: {file_name}", "success")

        # 检查文件格式
        try:
            # 尝试读取文件，验证是否为有效的Excel文件
            xl = pd.ExcelFile(file_path)
            sheet_names = xl.sheet_names
            self.log_message(f"Excel文件包含工作表: {', '.join(sheet_names)}", "info")

            # 检查是否包含所需的工作表
            if "基本组合内力" in sheet_names:
                self.log_message("✓ 找到所需工作表: '基本组合内力'", "success")
            else:
                self.log_message("⚠ 警告: 未找到工作表 '基本组合内力'", "warning")
        except Exception as e:
            self.log_message(f"⚠ 文件格式验证失败: {str(e)}", "warning")

    def select_file(self):
        """选择文件（通过文件对话框）"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择YJK表格文件",
            "",  # 默认路径为空
            "Excel文件 (*.xlsx *.xls);;所有文件 (*.*)")

        if file_path:
            self.set_file(file_path)

    def dragEnterEvent(self, event):
        """处理拖拽进入事件"""
        if event.mimeData().hasUrls():
            # 检查拖拽的文件中是否包含Excel文件
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        """处理拖放事件"""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                
                # 检查文件是否存在且是Excel文件
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                        try:
                            # 使用pandas验证文件
                            pd.read_excel(file_path, nrows=1)
                            self.set_file(file_path)
                            self.log_message(f"已通过拖放导入文件: {os.path.basename(file_path)}", "success")
                            event.acceptProposedAction()
                            return
                        except Exception as e:
                            self.log_message(f"✗ 文件读取失败: {str(e)}", "error")
                            QMessageBox.critical(self, "文件读取错误", f"无法读取拖放的文件: {str(e)}")
        
        event.ignore()



    def format_selection_dialog(self):
        """弹出格式选择对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("选择导出格式")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        label = QLabel("请选择导出文件格式:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # 按钮组
        button_group = QButtonGroup(dialog)
        
        # Excel格式
        excel_radio = QRadioButton("Excel格式 (.xlsx)")
        excel_radio.setChecked(True)
        button_group.addButton(excel_radio)
        layout.addWidget(excel_radio)
        
        # TXT格式
        txt_radio = QRadioButton("文本格式 (.txt)")
        button_group.addButton(txt_radio)
        layout.addWidget(txt_radio)
        
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        
        # 居中显示
        dialog.exec_()
        
        # 返回选择的格式
        if excel_radio.isChecked():
            return "xlsx"
        else:
            return "txt"

    def process_pressure(self):
        """处理压力数据"""
        if not self.file_path:
            self.log_message("⚠ 请先选择Excel文件", "error")
            QMessageBox.warning(self, "错误", "请先选择Excel文件")
            return

        try:
            self.log_message("开始处理压力数据...", "info")
            self.export_pressure_btn.setEnabled(False)
            
            # 执行处理
            result = self._logic.process_pressure(self.file_path)
            
            if result["success"]:
                # 显示成功信息
                success_msg = f"""
                <b>处理完成！</b><br><br>
                <b>原始数据行数:</b> {result['original_rows']}<br>
                <b>删除F列=1的行数:</b> {result['removed_rows']}<br>
                <b>最终压力数据行数:</b> {result['final_rows']}<br>
                <b>保存路径:</b> {result['save_path']}<br><br>
                <i>文件格式: {result['format'].upper()}</i>
                """
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("处理成功")
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(success_msg)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                
                self.log_message(f"✓ 压力数据已保存到: {result['save_path']}", "success")
                
                # 打开文件所在文件夹
                try:
                    os.startfile(os.path.dirname(result['save_path']))
                except Exception as e:
                    self.log_message(f"⚠ 打开文件夹失败: {str(e)}", "warning")
            else:
                raise ValueError(result["error"])

        except Exception as e:
            self.log_message(f"✗ 错误: {str(e)}", "error")
            QMessageBox.critical(self, "处理错误", str(e))
        finally:
            self.export_pressure_btn.setEnabled(True)

    def process_tension(self):
        """处理拉力数据"""
        if not self.file_path:
            self.log_message("⚠ 请先选择Excel文件", "error")
            QMessageBox.warning(self, "错误", "请先选择Excel文件")
            return

        try:
            self.log_message("开始处理拉力数据...", "info")
            self.export_tension_btn.setEnabled(False)
            
            # 执行处理
            result = self._logic.process_tension(self.file_path)
            
            if result["success"]:
                # 显示成功信息
                success_msg = f"""
                <b>处理完成！</b><br><br>
                <b>原始数据行数:</b> {result['original_rows']}<br>
                <b>删除F列=1的行数:</b> {result['removed_rows']}<br>
                <b>最终拉力数据行数:</b> {result['final_rows']}<br>
                <b>保存路径:</b> {result['save_path']}<br><br>
                <i>文件格式: {result['format'].upper()}</i>
                """
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("处理成功")
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(success_msg)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                
                self.log_message(f"✓ 拉力数据已保存到: {result['save_path']}", "success")
                
                # 打开文件所在文件夹
                try:
                    os.startfile(os.path.dirname(result['save_path']))
                except Exception as e:
                    self.log_message(f"⚠ 打开文件夹失败: {str(e)}", "warning")
            else:
                raise ValueError(result["error"])

        except Exception as e:
            self.log_message(f"✗ 错误: {str(e)}", "error")
            QMessageBox.critical(self, "处理错误", str(e))
        finally:
            self.export_tension_btn.setEnabled(True)

    def process_all(self):
        """处理全部柱底内力"""
        if not self.file_path:
            self.log_message("⚠ 请先选择Excel文件", "error")
            QMessageBox.warning(self, "错误", "请先选择Excel文件")
            return

        try:
            self.log_message("开始处理全部柱底内力数据...", "info")
            self.export_all_btn.setEnabled(False)
            
            # 执行处理
            result = self._logic.process_all(self.file_path)
            
            if result["success"]:
                # 显示成功信息
                success_msg = f"""
                <b>处理完成！</b><br><br>
                <b>原始数据行数:</b> {result['original_rows']}<br>
                <b>删除F列=1的行数:</b> {result['removed_rows']}<br>
                <b>最终数据行数:</b> {result['final_rows']}<br>
                <b>保存路径:</b> {result['save_path']}<br><br>
                <i>文件格式: {result['format'].upper()}</i>
                """
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("处理成功")
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(success_msg)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                
                self.log_message(f"✓ 全部柱底内力数据已保存到: {result['save_path']}", "success")
                
                # 打开文件所在文件夹
                try:
                    os.startfile(os.path.dirname(result['save_path']))
                except Exception as e:
                    self.log_message(f"⚠ 打开文件夹失败: {str(e)}", "warning")
            else:
                raise ValueError(result["error"])

        except Exception as e:
            self.log_message(f"✗ 错误: {str(e)}", "error")
            QMessageBox.critical(self, "处理错误", str(e))
        finally:
            self.export_all_btn.setEnabled(True)
    
    def _on_original_mode_clicked(self):
        """切换到原版模式"""
        if self._current_mode != "original":
            self._current_mode = "original"
            # 恢复标题
            self.title_label.setText("YJK柱脚内力格式调整工具")
            
            # 恢复按钮文本和功能
            self.export_pressure_btn.setText("📤 导出全部压力数据")
            self.export_pressure_btn.clicked.disconnect()
            self.export_pressure_btn.clicked.connect(self.process_pressure)
            
            self.export_tension_btn.setText("📤 导出全部拉力数据")
            self.export_tension_btn.clicked.disconnect()
            self.export_tension_btn.clicked.connect(self.process_tension)
            
            self.export_all_btn.setText("📤 导出全部柱底内力")
            self.export_all_btn.clicked.disconnect()
            self.export_all_btn.clicked.connect(self.process_all)
            
            # 更新按钮状态
            self.original_mode_btn.setChecked(True)
            self.explorer_mode_btn.setChecked(False)
            
            self.log_message("已切换到原版柱底力导出模式", "success")
    
    def _on_explorer_mode_clicked(self):
        """切换到探索者模式"""
        if self._current_mode != "explorer":
            self._current_mode = "explorer"
            # 更新标题
            self.title_label.setText("探索者柱底力导出")
            
            # 更新按钮文本和功能
            self.export_pressure_btn.setText("📤 导出探索者压力数据")
            self.export_pressure_btn.clicked.disconnect()
            self.export_pressure_btn.clicked.connect(self.process_explorer_pressure)
            
            self.export_tension_btn.setText("📤 导出探索者拉力数据")
            self.export_tension_btn.clicked.disconnect()
            self.export_tension_btn.clicked.connect(self.process_explorer_tension)
            
            self.export_all_btn.setText("📤 导出探索者全部内力")
            self.export_all_btn.clicked.disconnect()
            self.export_all_btn.clicked.connect(self.process_explorer_all)
            
            # 更新按钮状态
            self.original_mode_btn.setChecked(False)
            self.explorer_mode_btn.setChecked(True)
            
            self.log_message("已切换到探索者柱底力导出模式", "success")
    
    def process_explorer_pressure(self):
        """处理探索者压力数据"""
        self.export_explorer_data("pressure")
    
    def process_explorer_tension(self):
        """处理探索者拉力数据"""
        self.export_explorer_data("tension")
    
    def process_explorer_all(self):
        """处理探索者全部内力数据"""
        self.export_explorer_data("all")
    
    def export_explorer_data(self, export_type):
        """导出探索者数据"""
        if not self.file_path:
            self.log_message("⚠ 请先选择Excel文件", "error")
            QMessageBox.warning(self, "错误", "请先选择Excel文件")
            return
        
        try:
            self.log_message(f"开始处理探索者{export_type}数据...", "info")
            
            # 禁用所有按钮
            self.export_pressure_btn.setEnabled(False)
            self.export_tension_btn.setEnabled(False)
            self.export_all_btn.setEnabled(False)
            
            # 读取Excel文件
            self.log_message("尝试读取Excel文件...", "info")
            
            # 调用逻辑层处理
            result = self._logic.export_explorer_data(self.file_path, export_type)
            
            if result["success"]:
                # 显示成功信息
                success_msg = f"""
                <b>处理完成！</b><br><br>
                <b>原始数据行数:</b> {result['original_rows']}<br>
                <b>删除F列=1的行数:</b> {result['removed_rows']}<br>
                <b>最终数据行数:</b> {result['final_rows']}<br>
                <b>保存路径:</b> {result['save_path']}<br><br>
                <i>文件格式: {result['format'].upper()}</i>
                """
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("处理成功")
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(success_msg)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                
                self.log_message(f"✓ 探索者{export_type}数据已保存到: {result['save_path']}", "success")
                
                # 打开文件所在文件夹
                try:
                    os.startfile(os.path.dirname(result['save_path']))
                except Exception as e:
                    self.log_message(f"⚠ 打开文件夹失败: {str(e)}", "warning")
            else:
                raise ValueError(result["error"])

        except Exception as e:
            self.log_message(f"✗ 错误: {str(e)}", "error")
            QMessageBox.critical(self, "处理错误", str(e))
        finally:
            # 启用所有按钮
            self.export_pressure_btn.setEnabled(True)
            self.export_tension_btn.setEnabled(True)
            self.export_all_btn.setEnabled(True)

    def reset(self):
        """重置插件UI到初始状态"""
        # 清空文件信息
        self.file_info_label.setText("未选择文件")
        self.file_info_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 15px;
                min-height: 70px;
                color: #495057;
            }
        """)
        
        # 禁用按钮
        self.export_pressure_btn.setEnabled(False)
        self.export_tension_btn.setEnabled(False)
        self.export_all_btn.setEnabled(False)
        
        # 清空日志
        self.log_text.clear()
        
        # 清空文件路径
        self.file_path = ""
