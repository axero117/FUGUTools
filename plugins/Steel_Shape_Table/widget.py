"""型钢特性表插件UI组件"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QSplitter,
    QGroupBox
)
from PySide6.QtCore import Signal, Slot, Qt

from plugins.Steel_Shape_Table.logic import SteelShapeLogic
from plugins.Steel_Shape_Table.ui.section_diagram import SectionDiagram


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
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(title_label)
        
        # 搜索和类型选择区域
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        # 型钢类型选择
        type_label = QLabel("型钢类型：")
        self._type_combo = QComboBox()
        self._type_combo.setMinimumWidth(150)
        
        # 添加型钢类型选项
        shape_types = self._logic.get_shape_types()
        self._type_combo.addItems(shape_types)
        
        # 搜索框
        search_label = QLabel("搜索：")
        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("输入型号关键词，如100")
        self._search_edit.setMinimumWidth(200)
        
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
        self._table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 表格不可编辑
        self._table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # 选中整行
        self._table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # 单选
        
        # 设置表格标题
        self._table_widget.setColumnCount(11)
        self._table_widget.setHorizontalHeaderLabels([
            "型号", "高度H(mm)", "宽度B(mm)", "腹板厚度t1(mm)", "翼缘厚度t2(mm)",
            "截面面积(cm²)", "理论重量(kg/m)", "惯性矩Ix(cm⁴)", "惯性矩Iy(cm⁴)",
            "截面模量Wx(cm³)", "截面模量Wy(cm³)"
        ])
        
        # 设置表头自适应
        header = self._table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        left_layout.addWidget(self._table_widget)
        
        # 右侧：截面形状绘图区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # 添加截面形状标题
        diagram_title = QLabel("截面形状")
        diagram_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        right_layout.addWidget(diagram_title)
        
        # 创建截面形状绘图组件
        self._section_diagram = SectionDiagram()
        right_layout.addWidget(self._section_diagram)
        
        # 添加控制按钮
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        # 重置视图按钮
        reset_btn = QPushButton("重置视图")
        reset_btn.clicked.connect(self._section_diagram.reset_view)
        control_layout.addWidget(reset_btn)
        
        # 缩放控制
        zoom_in_btn = QPushButton("放大")
        zoom_in_btn.clicked.connect(lambda: self._section_diagram.set_scale_factor(self._section_diagram._scale_factor * 1.2))
        control_layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton("缩小")
        zoom_out_btn.clicked.connect(lambda: self._section_diagram.set_scale_factor(self._section_diagram._scale_factor * 0.8))
        control_layout.addWidget(zoom_out_btn)
        
        control_layout.addStretch()
        right_layout.addLayout(control_layout)
        
        # 添加提示信息
        tip_label = QLabel("提示：鼠标滚轮缩放，左键拖拽平移")
        tip_label.setStyleSheet("font-size: 12px; color: #666; margin-top: 5px;")
        right_layout.addWidget(tip_label)
        
        # 添加到分割器
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        
        # 设置分割比例
        main_splitter.setStretchFactor(0, 2)  # 左侧占2/3
        main_splitter.setStretchFactor(1, 1)  # 右侧占1/3
        
        # 设置主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_splitter)
        
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
        self._table_widget.itemSelectionChanged.connect(self._on_table_selection_changed)
        
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
        
        # 添加数据到表格
        for i, shape in enumerate(shapes):
            self._table_widget.insertRow(i)
            
            # 填充数据
            self._table_widget.setItem(i, 0, QTableWidgetItem(shape["型号"]))
            
            # 数值类型的数据设置为右对齐
            for col, key in enumerate(["高度H", "宽度B", "腹板厚度t1", "翼缘厚度t2", "截面面积", "理论重量", "惯性矩Ix", "惯性矩Iy", "截面模量Wx", "截面模量Wy"], 1):
                if key in shape:
                    item = QTableWidgetItem(f"{shape[key]:.2f}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self._table_widget.setItem(i, col, item)
    
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
        
        # 提取数值参数
        headers = ["高度H", "宽度B", "腹板厚度t1", "翼缘厚度t2", "截面面积", "理论重量", "惯性矩Ix", "惯性矩Iy", "截面模量Wx", "截面模量Wy"]
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