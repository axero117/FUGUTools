"""型钢特性表插件UI组件"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox, QLineEdit, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton,
                               QMessageBox, QScrollArea, QSplitter, QGroupBox,
                               QDialog)
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QFont

from plugins.Steel_Shape_Table.logic import SteelShapeLogic
from plugins.Steel_Shape_Table.ui.section_diagram import SectionDiagram
from plugins.Steel_Shape_Table.table_config import get_table_config


class SteelShapeTableWidget(QWidget):
    """型钢特性表插件UI组件"""

    # 定义信号：标签标题变化
    title_changed = Signal(str)

    def __init__(self):
        """初始化UI组件"""
        super().__init__()

        # 初始化业务逻辑
        self._logic = SteelShapeLogic()

        # 初始化当前型钢类型（先初始化，避免在_load_shapes中使用时报错）
        self._current_shape_type = ""

        # 初始化UI
        self._init_ui()

        # 连接信号和槽
        self._connect_signals()

    def _init_ui(self):
        """初始化UI"""
        # 创建主分割器
        main_splitter = QSplitter(Qt.Horizontal, self)

        # 左侧：搜索和表格区域
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # 添加标题
        title_label = QLabel("型钢特性表")
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(title_label)

        # 搜索和类型选择区域
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        # 型钢类型选择
        type_label = QLabel("型钢类型：")
        self._type_combo = QComboBox()
        self._type_combo.setMinimumWidth(250)

        # 添加型钢类型选项
        shape_types = self._logic.get_shape_types()
        self._type_combo.addItems(shape_types)

        # 搜索框
        search_label = QLabel("搜索：")
        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("输入型号关键词，如100")
        self._search_edit.setMinimumWidth(70)

        # 搜索按钮
        self._search_btn = QPushButton("搜索")

        # 添加到搜索布局
        search_layout.addWidget(type_label)
        search_layout.addWidget(self._type_combo)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self._search_edit)
        search_layout.addWidget(self._search_btn)
        search_layout.addStretch()

        left_layout.addLayout(search_layout)

        # 型钢特性表
        self._table_widget = QTableWidget()
        self._table_widget.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)  # 表格不可编辑
        self._table_widget.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)  # 选中整行
        self._table_widget.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection)  # 单选

        # 设置表格标题
        self._table_widget.setColumnCount(16)
        self._table_widget.setHorizontalHeaderLabels([
            "型号", "高度H(mm)", "宽度B(mm)", "腹板厚度t1(mm)", "翼缘厚度t2(mm)",
            "圆角半径r(mm)", "内圆角半径r'(mm)", "截面面积(cm²)", "理论重量(kg/m)", "表面积(m²/m)",
            "惯性矩Ix(cm⁴)", "惯性矩Iy(cm⁴)", "惯性半径rx(cm)", "惯性半径ry(cm)",
            "截面模量Wx(cm³)", "截面模量Wy(cm³)"
        ])

        # 设置表头自适应
        header = self._table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # 设置表头字体大小
        header_font = QFont()
        header_font.setPointSize(15)  # 设置表头字体大小为15
        header.setFont(header_font)

        # 应用样式表以确保视觉效果（仅针对表头）
        header.setStyleSheet("QHeaderView::section {"
                             "    font-size: 15px;"
                             "    font-weight: bold;"
                             "    padding: 4px;"
                             "    white-space: pre-wrap;"
                             "}")

        left_layout.addWidget(self._table_widget)

        # 添加到分割器
        main_splitter.addWidget(left_widget)

        # 设置主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_splitter)

        # 添加表格行双击事件
        self._table_widget.itemDoubleClicked.connect(
            self._on_table_item_clicked)

        # 初始化截面形状组件
        self._section_diagram = SectionDiagram()

        # 初始化表格数据
        self._load_shapes()

    def _connect_signals(self):
        """连接信号和槽"""
        # 连接类型选择变化信号
        self._type_combo.currentTextChanged.connect(self._load_shapes)

        # 连接搜索按钮点击信号
        self._search_btn.clicked.connect(self._load_shapes)

        # 连接搜索框回车键信号
        self._search_edit.returnPressed.connect(self._load_shapes)

        # 连接表格选择变化信号
        self._table_widget.itemSelectionChanged.connect(
            self._on_table_selection_changed)

        # 发出初始标题信号（延迟发出，确保界面已完全初始化）
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._emit_initial_title)

    @Slot()
    def _load_shapes(self):
        """加载型钢数据到表格"""
        shape_type = self._type_combo.currentText()
        keyword = self._search_edit.text().strip()

        # 检查型钢类型是否发生变化
        if shape_type != self._current_shape_type:
            self._current_shape_type = shape_type
            # 发出标题变化信号
            self.title_changed.emit(f"{shape_type}型钢特性表")

        # 获取型钢数据
        shapes = self._logic.search_shapes(shape_type, keyword)

        # 清空表格
        self._table_widget.setRowCount(0)

        # 获取当前表类型的列配置
        column_config, table_name = get_table_config(shape_type)

        if column_config:
            # 设置表格列数
            self._table_widget.setColumnCount(len(column_config))

            # 设置表格标题
            headers = [title for _, title, _ in column_config]
            self._table_widget.setHorizontalHeaderLabels(headers)

            # 重新设置表头自适应
            header = self._table_widget.horizontalHeader()
            header.setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents)

            # 重新设置表头字体大小（确保在更改表头后仍然生效）
            header_font = QFont()
            header_font.setPointSize(15)  # 设置表头字体大小为15，以保持一致性
            header.setFont(header_font)

            # 应用样式表以确保视觉效果（仅针对表头）
            header.setStyleSheet("QHeaderView::section {"
                                 "    font-size: 15px;"
                                 "    font-weight: bold;"
                                 "    padding: 4px;"
                                 "    white-space: pre-wrap;"
                                 "}")

            # 记录当前表类型（用于选择变化时提取数据）
            self._current_table_name = table_name

            # 添加数据到表格
            for i, shape in enumerate(shapes):
                self._table_widget.insertRow(i)

                # 填充数据
                for col, (db_col, title, fmt) in enumerate(column_config):
                    # 严格匹配字段名
                    found_key = db_col if db_col in shape else None
                    if found_key and shape[found_key] is not None:
                        value = shape[found_key]
                        if fmt == 's':
                            item = QTableWidgetItem(str(value))
                        else:
                            # 使用 format 方法格式化数字
                            format_str = "{:" + fmt + "}"
                            formatted_value = format_str.format(value)
                            item = QTableWidgetItem(formatted_value)
                            item.setTextAlignment(
                                Qt.AlignmentFlag.AlignRight
                                | Qt.AlignmentFlag.AlignVCenter)
                        # 设置表格内容字体大小为10
                        item_font = QFont()
                        item_font.setPointSize(10)
                        item.setFont(item_font)
                        self._table_widget.setItem(i, col, item)
        else:
            # 如果没有配置，则显示错误信息而不是使用默认配置
            # 仍然设置基本的表头以避免错误
            self._table_widget.setColumnCount(1)
            self._table_widget.setHorizontalHeaderLabels(["暂无数据"])
            self._current_table_name = None

    @Slot()
    def _on_table_selection_changed(self):
        """处理表格选择变化"""
        # 获取当前选中的行
        selected_items = self._table_widget.selectedItems()
        if not selected_items:
            return

        # 获取选中行的数据
        row = selected_items[0].row()
        shape_data = {}

        # 从表格中提取数据
        shape_data["型号"] = self._table_widget.item(row, 0).text()

        # 获取型钢类型
        shape_data["类型"] = self._type_combo.currentText()

        # 获取当前表类型的列配置
        column_config, table_name = get_table_config(
            self._type_combo.currentText())

        if column_config:
            # 根据列配置提取数据
            for col, (db_col, title, fmt) in enumerate(column_config):
                item = self._table_widget.item(row, col)
                if item and item.text():
                    try:
                        shape_data[title] = float(item.text())
                    except ValueError:
                        pass
        else:
            headers = [
                "高度H", "宽度B", "腹板厚度t1", "翼缘厚度t2", "圆角半径r", "内圆角半径r'", "截面面积",
                "理论重量", "表面积", "惯性矩Ix", "惯性矩Iy", "惯性半径rx", "惯性半径ry", "截面模量Wx",
                "截面模量Wy"
            ]
            for i, header in enumerate(headers, 1):
                item = self._table_widget.item(row, i)
                if item and item.text():
                    try:
                        shape_data[header] = float(item.text())
                    except ValueError:
                        pass

        # 更新截面形状图
        self._section_diagram.set_shape_data(shape_data)

    def _emit_initial_title(self):
        """发出初始标题信号"""
        initial_shape_type = self._type_combo.currentText()
        if initial_shape_type:
            self.title_changed.emit(f"{initial_shape_type}型钢特性表")

    def reset(self):
        """重置界面"""
        # 重置类型选择
        self._type_combo.setCurrentIndex(0)

        # 清空搜索框
        self._search_edit.clear()

        # 重新加载数据
        self._load_shapes()

        # 清空截面图
        self._section_diagram.set_shape_data(None)

    def _get_shape_type_name(self, shape_type):
        """获取型钢类型名称

        Args:
            shape_type: 型钢类型字符串

        Returns:
            str: 简化的类型名称
        """
        if "H型钢" in shape_type:
            return "H型钢"
        elif "工字钢" in shape_type or "I型钢" in shape_type:
            return "工字钢"
        elif "槽钢" in shape_type or "C型钢" in shape_type:
            return "槽钢"
        elif "角钢" in shape_type:
            return "角钢"
        else:
            return ""

    def _on_table_item_clicked(self, item):
        """表格项点击事件

        Args:
            item: 点击的表格项
        """
        # 获取当前行
        row = item.row()

        # 获取当前表类型
        shape_type = self._type_combo.currentText()

        # 获取当前表的数据
        keyword = self._search_edit.text()
        shapes = self._logic.search_shapes(shape_type, keyword)

        if row < len(shapes):
            # 获取点击行的数据
            shape_data = shapes[row]

            # 创建截面形状对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(f"{shape_data.get('model')} - 截面形状")
            dialog.resize(600, 400)

            # 创建对话框布局
            dialog_layout = QVBoxLayout(dialog)
            dialog_layout.setSpacing(10)
            dialog_layout.setContentsMargins(10, 10, 10, 10)

            # 添加截面形状标题
            diagram_title = QLabel("截面形状")
            diagram_title.setStyleSheet(
                "font-size: 16px; font-weight: bold; margin-bottom: 5px;")
            dialog_layout.addWidget(diagram_title)

            # 创建临时截面形状绘图组件
            temp_diagram = SectionDiagram()
            dialog_layout.addWidget(temp_diagram)

            # 添加控制按钮
            control_layout = QHBoxLayout()
            control_layout.setSpacing(10)

            # 重置视图按钮
            reset_btn = QPushButton("重置视图")
            reset_btn.clicked.connect(temp_diagram.reset_view)
            control_layout.addWidget(reset_btn)

            # 缩放控制
            zoom_in_btn = QPushButton("放大")
            zoom_in_btn.clicked.connect(lambda: temp_diagram.set_scale_factor(
                temp_diagram._scale_factor * 1.2))
            control_layout.addWidget(zoom_in_btn)

            zoom_out_btn = QPushButton("缩小")
            zoom_out_btn.clicked.connect(lambda: temp_diagram.set_scale_factor(
                temp_diagram._scale_factor * 0.8))
            control_layout.addWidget(zoom_out_btn)

            control_layout.addStretch()
            dialog_layout.addLayout(control_layout)

            # 添加提示信息
            tip_label = QLabel("提示：鼠标滚轮缩放，左键拖拽平移")
            tip_label.setStyleSheet(
                "font-size: 12px; color: #666; margin-top: 5px;")
            dialog_layout.addWidget(tip_label)

            # 转换类型名称并更新截面形状
            shape_data_with_type = shape_data.copy()
            shape_data_with_type["类型"] = self._get_shape_type_name(shape_type)
            temp_diagram.set_shape_data(shape_data_with_type)

            # 显示对话框
            dialog.exec_()
