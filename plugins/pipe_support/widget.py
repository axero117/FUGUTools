"""管墩计算插件UI组件"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QGroupBox,
    QComboBox,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QPushButton,
    QSpacerItem
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Slot, Qt

from plugins.pipe_support.logic import PipeSupportLogic


class PipeSupportWidget(QWidget):
    """管墩计算插件UI组件"""
    
    def __init__(self):
        """初始化UI组件"""
        super().__init__()
        
        # 初始化业务逻辑
        self._logic = PipeSupportLogic()
        
        # 初始化UI
        self._init_ui()
        
        # 连接信号和槽
        self._connect_signals()
    
    def _init_ui(self):
        """初始化UI"""
        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 滚动区域的容器Widget
        scroll_widget = QWidget()
        
        # 主布局：垂直布局，包含标题、参数区域和结果区域
        main_layout = QVBoxLayout(scroll_widget)
        
        # 添加标题
        title_label = QLabel("管墩计算")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)  # 设置文字居中
        main_layout.addWidget(title_label)
        
        # 参数区域：水平布局，左侧是基础尺寸+预埋钢板参数，右侧是基础形式+荷载参数+计算按钮
        params_layout = QHBoxLayout()
        
        # 左侧列：基础尺寸 + 预埋钢板参数（垂直排列）
        outer_left_column = QVBoxLayout()
        
        # 基础尺寸输入组
        base_size_group = QGroupBox("基础尺寸")
        base_size_group.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        base_size_group.setMaximumWidth(500)  # 缩小最大宽度
        # 设置组标题背景透明
        base_size_group.setStyleSheet("QGroupBox { background-color: transparent; }")
        base_size_layout = QVBoxLayout(base_size_group)
        
        # 单位标签宽度
        unit_label_width = 30
        
        # 创建两列布局
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(15)  # 缩小列间距
        
        # 标签宽度
        label_width = 100
        
        # 左侧列
        left_column = QVBoxLayout()
        left_column.setSpacing(8)  # 缩小垂直间距
        
        # 底板长度
        self._base_length_layout = QHBoxLayout()
        self._base_length_layout.setSpacing(10)
        label = QLabel("底板长度:")
        label.setFixedWidth(label_width)
        self._base_length_layout.addWidget(label)
        self._base_length_edit = QLineEdit()
        self._base_length_layout.addWidget(self._base_length_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_length_layout.addWidget(unit_label)
        left_column.addLayout(self._base_length_layout)
        
        # 底板宽度
        self._base_bottom_width_layout = QHBoxLayout()
        self._base_bottom_width_layout.setSpacing(10)
        label = QLabel("底板宽度:")
        label.setFixedWidth(label_width)
        self._base_bottom_width_layout.addWidget(label)
        self._base_bottom_width_edit = QLineEdit()
        self._base_bottom_width_layout.addWidget(self._base_bottom_width_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_bottom_width_layout.addWidget(unit_label)
        left_column.addLayout(self._base_bottom_width_layout)
        
        # 基础短柱长度
        self._base_column_length_layout = QHBoxLayout()
        self._base_column_length_layout.setSpacing(10)
        label = QLabel("基础短柱长度:")
        label.setFixedWidth(label_width)
        self._base_column_length_layout.addWidget(label)
        self._base_column_length_edit = QLineEdit()
        self._base_column_length_layout.addWidget(self._base_column_length_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_column_length_layout.addWidget(unit_label)
        left_column.addLayout(self._base_column_length_layout)
        
        # 基础短柱宽度
        self._base_column_width_layout = QHBoxLayout()
        self._base_column_width_layout.setSpacing(10)
        label = QLabel("基础短柱宽度:")
        label.setFixedWidth(label_width)
        self._base_column_width_layout.addWidget(label)
        self._base_column_width_edit = QLineEdit()
        self._base_column_width_layout.addWidget(self._base_column_width_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_column_width_layout.addWidget(unit_label)
        left_column.addLayout(self._base_column_width_layout)
        
        # 基础顶面宽度
        self._base_top_width_layout = QHBoxLayout()
        self._base_top_width_layout.setSpacing(10)
        label = QLabel("基础顶面宽度:")
        label.setFixedWidth(label_width)
        self._base_top_width_layout.addWidget(label)
        self._base_top_width_edit = QLineEdit()
        self._base_top_width_layout.addWidget(self._base_top_width_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_top_width_layout.addWidget(unit_label)
        left_column.addLayout(self._base_top_width_layout)
        
        # 基础高度
        self._base_height_layout = QHBoxLayout()
        self._base_height_layout.setSpacing(10)
        label = QLabel("基础高度:")
        label.setFixedWidth(label_width)
        self._base_height_layout.addWidget(label)
        self._base_height_edit = QLineEdit()
        self._base_height_layout.addWidget(self._base_height_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_height_layout.addWidget(unit_label)
        left_column.addLayout(self._base_height_layout)
        
        # 右侧列
        right_column = QVBoxLayout()
        right_column.setSpacing(8)  # 缩小垂直间距
        
        # 基础高出地面高度
        self._base_height_above_ground_layout = QHBoxLayout()
        self._base_height_above_ground_layout.setSpacing(10)
        label = QLabel("基础高出地面\n高度:")
        label.setFixedWidth(label_width)
        self._base_height_above_ground_layout.addWidget(label)
        self._base_height_above_ground_edit = QLineEdit()
        self._base_height_above_ground_layout.addWidget(self._base_height_above_ground_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._base_height_above_ground_layout.addWidget(unit_label)
        right_column.addLayout(self._base_height_above_ground_layout)
        
        # 垫层厚度（单位改为mm）
        self._cushion_thickness_layout = QHBoxLayout()
        self._cushion_thickness_layout.setSpacing(10)
        label = QLabel("垫层厚度:")
        label.setFixedWidth(label_width)
        self._cushion_thickness_layout.addWidget(label)
        self._cushion_thickness_edit = QLineEdit()
        self._cushion_thickness_layout.addWidget(self._cushion_thickness_edit)
        unit_label = QLabel("mm")
        unit_label.setFixedWidth(unit_label_width)
        self._cushion_thickness_layout.addWidget(unit_label)
        right_column.addLayout(self._cushion_thickness_layout)
        
        # 换填级配砂石厚度
        self._replacement_thickness_layout = QHBoxLayout()
        self._replacement_thickness_layout.setSpacing(10)
        label = QLabel("换填级配砂石\n厚度:")
        label.setFixedWidth(label_width)
        self._replacement_thickness_layout.addWidget(label)
        self._replacement_thickness_edit = QLineEdit()
        self._replacement_thickness_layout.addWidget(self._replacement_thickness_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._replacement_thickness_layout.addWidget(unit_label)
        right_column.addLayout(self._replacement_thickness_layout)
        
        # 换填级配砂石宽度
        self._replacement_width_layout = QHBoxLayout()
        self._replacement_width_layout.setSpacing(10)
        label = QLabel("换填级配砂石\n宽度:")
        label.setFixedWidth(label_width)
        self._replacement_width_layout.addWidget(label)
        self._replacement_width_edit = QLineEdit()
        self._replacement_width_layout.addWidget(self._replacement_width_edit)
        unit_label = QLabel("m")
        unit_label.setFixedWidth(unit_label_width)
        self._replacement_width_layout.addWidget(unit_label)
        right_column.addLayout(self._replacement_width_layout)
        
        # 基础数量
        self._foundation_count_layout = QHBoxLayout()
        self._foundation_count_layout.setSpacing(10)
        label = QLabel("基础数量:")
        label.setFixedWidth(label_width)
        self._foundation_count_layout.addWidget(label)
        self._foundation_count_edit = QLineEdit()
        self._foundation_count_layout.addWidget(self._foundation_count_edit)
        unit_label = QLabel("个")
        unit_label.setFixedWidth(unit_label_width)
        self._foundation_count_layout.addWidget(unit_label)
        right_column.addLayout(self._foundation_count_layout)
        
        # 将左右列添加到两列布局
        columns_layout.addLayout(left_column)
        columns_layout.addLayout(right_column)
        
        # 将两列布局添加到基础尺寸布局
        base_size_layout.addLayout(columns_layout)
        
        outer_left_column.addWidget(base_size_group)
        
        # 预埋钢板参数输入组
        embedded_plate_group = QGroupBox("预埋钢板参数")
        embedded_plate_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # 设置组标题背景透明
        embedded_plate_group.setStyleSheet("QGroupBox { background-color: transparent; }")
        embedded_plate_layout = QHBoxLayout(embedded_plate_group)
        
        # 预埋钢板长度
        self._plate_length_layout = QHBoxLayout()
        self._plate_length_layout.addWidget(QLabel("长度:"))
        self._plate_length_edit = QLineEdit()
        self._plate_length_layout.addWidget(self._plate_length_edit)
        self._plate_length_layout.addWidget(QLabel("m"))
        embedded_plate_layout.addLayout(self._plate_length_layout)
        
        # 预埋钢板宽度
        self._plate_width_layout = QHBoxLayout()
        self._plate_width_layout.addWidget(QLabel("宽度:"))
        self._plate_width_edit = QLineEdit()
        self._plate_width_layout.addWidget(self._plate_width_edit)
        self._plate_width_layout.addWidget(QLabel("m"))
        embedded_plate_layout.addLayout(self._plate_width_layout)
        
        # 预埋钢板厚度
        self._plate_thickness_layout = QHBoxLayout()
        self._plate_thickness_layout.addWidget(QLabel("厚度:"))
        self._plate_thickness_edit = QLineEdit()
        self._plate_thickness_layout.addWidget(self._plate_thickness_edit)
        self._plate_thickness_layout.addWidget(QLabel("mm"))
        embedded_plate_layout.addLayout(self._plate_thickness_layout)
        
        # 创建预埋钢板布局
        plate_layout = QHBoxLayout()
        plate_layout.addWidget(embedded_plate_group)
        
        outer_left_column.addLayout(plate_layout)
        
        # 其它参数输入组
        pipe_support_form_group = QGroupBox("其它参数")
        pipe_support_form_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # 设置组标题背景透明
        pipe_support_form_group.setStyleSheet("QGroupBox { background-color: transparent; }")
        pipe_support_form_layout = QHBoxLayout(pipe_support_form_group)
        pipe_support_form_layout.setSpacing(20)  # 设置间距
        
        # 管墩形式选择
        self._pipe_support_type_layout = QHBoxLayout()
        self._pipe_support_type_layout.addWidget(QLabel("管墩形式:"))
        self._pipe_support_type_combo = QComboBox()
        self._pipe_support_type_combo.addItems(["固定墩", "活动墩"])
        # 默认选择固定墩
        self._pipe_support_type_combo.setCurrentText("固定墩")
        self._pipe_support_type_layout.addWidget(self._pipe_support_type_combo)
        pipe_support_form_layout.addLayout(self._pipe_support_type_layout)
        
        # 是否考虑地下水选择
        self._consider_groundwater_layout = QHBoxLayout()
        self._consider_groundwater_layout.addWidget(QLabel("是否考虑地下水:"))
        self._consider_groundwater_combo = QComboBox()
        self._consider_groundwater_combo.addItems(["否", "是"])
        # 默认选择否
        self._consider_groundwater_combo.setCurrentText("否")
        self._consider_groundwater_layout.addWidget(self._consider_groundwater_combo)
        pipe_support_form_layout.addLayout(self._consider_groundwater_layout)
        
        # 创建管墩形式布局
        support_form_layout = QHBoxLayout()
        support_form_layout.addWidget(pipe_support_form_group)
        
        outer_left_column.addLayout(support_form_layout)
        
        # 添加伸缩空间，使左侧列高度与右侧列保持一致
        outer_left_column.addStretch()
        
        # 右侧列：添加基础形式组
        right_column = QVBoxLayout()
        
        # 基础形式输入组
        foundation_form_group = QGroupBox("基础形式")
        foundation_form_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # 设置组标题背景透明
        foundation_form_group.setStyleSheet("QGroupBox { background-color: transparent; }")
        foundation_form_layout = QVBoxLayout(foundation_form_group)
        
        # 基础样式选择
        self._foundation_style_layout = QHBoxLayout()
        self._foundation_style_layout.addWidget(QLabel("基础样式:"))
        self._foundation_style_combo = QComboBox()
        self._foundation_style_combo.addItems(["梯形基础", "T型基础"])
        # 默认选择T型基础
        self._foundation_style_combo.setCurrentText("T型基础")
        self._foundation_style_layout.addWidget(self._foundation_style_combo)
        foundation_form_layout.addLayout(self._foundation_style_layout)
        
        # 底板高度
        self._base_plate_height_layout = QHBoxLayout()
        self._base_plate_height_layout.addWidget(QLabel("底板高度:"))
        self._base_plate_height_edit = QLineEdit()
        # 默认启用底板高度输入框（T型基础）
        self._base_plate_height_edit.setEnabled(True)
        self._base_plate_height_layout.addWidget(self._base_plate_height_edit)
        self._base_plate_height_layout.addWidget(QLabel("m"))
        foundation_form_layout.addLayout(self._base_plate_height_layout)
        
        right_column.addWidget(foundation_form_group)
        
        # 荷载参数输入组
        load_params_group = QGroupBox("荷载参数")
        load_params_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # 设置组标题背景透明
        load_params_group.setStyleSheet("QGroupBox { background-color: transparent; }")
        load_params_layout = QVBoxLayout(load_params_group)
        
        # 上部垂直荷载
        self._upper_vertical_load_layout = QHBoxLayout()
        self._upper_vertical_load_layout.addWidget(QLabel("上部垂直荷载:"))
        self._upper_vertical_load_edit = QLineEdit()
        self._upper_vertical_load_layout.addWidget(self._upper_vertical_load_edit)
        self._upper_vertical_load_layout.addWidget(QLabel("KN"))
        load_params_layout.addLayout(self._upper_vertical_load_layout)
        
        # 上部水平荷载
        self._upper_horizontal_load_layout = QHBoxLayout()
        self._upper_horizontal_load_layout.addWidget(QLabel("上部水平荷载:"))
        self._upper_horizontal_load_edit = QLineEdit()
        self._upper_horizontal_load_layout.addWidget(self._upper_horizontal_load_edit)
        self._upper_horizontal_load_layout.addWidget(QLabel("KN"))
        load_params_layout.addLayout(self._upper_horizontal_load_layout)
        
        # 地基承载力
        self._bearing_capacity_layout = QHBoxLayout()
        self._bearing_capacity_layout.addWidget(QLabel("地基承载力:"))
        self._bearing_capacity_edit = QLineEdit()
        self._bearing_capacity_layout.addWidget(self._bearing_capacity_edit)
        self._bearing_capacity_layout.addWidget(QLabel("kPa"))
        load_params_layout.addLayout(self._bearing_capacity_layout)
        
        right_column.addWidget(load_params_group)
        
        # 计算按钮区域 - 垂直布局
        calculate_layout = QVBoxLayout()
        
        # 计算按钮
        self._calculate_btn = QPushButton("计算")
        self._calculate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498DB, stop:1 #2980B9);
                color: white;
                border: 1px solid #2471A3;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                min-width: 100px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3aade0, stop:1 #3498DB);
                border: 1px solid #2980B9;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2471A3, stop:1 #1f638c);
            }
        """)
        calculate_layout.addWidget(self._calculate_btn)
        
        # 导出计算书按钮
        self._export_btn = QPushButton("导出计算书")
        self._export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
                color: white;
                border: 1px solid #229954;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                min-width: 120px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #32e17c, stop:1 #2ecc71);
                border: 1px solid #27ae60;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #229954, stop:1 #1e8449);
            }
        """)
        calculate_layout.addWidget(self._export_btn)

        # 导出料表按钮
        self._export_material_btn = QPushButton("导出料表")
        self._export_material_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 1px solid #2471A3;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                min-width: 120px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5dade2, stop:1 #3498db);
                border: 1px solid #2980b9;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2471A3, stop:1 #1f638b);
            }
        """)
        calculate_layout.addWidget(self._export_material_btn)
        calculate_layout.addStretch()  # 添加弹簧使按钮顶部对齐
        
        right_column.addLayout(calculate_layout)
        
        # 添加伸缩空间
        right_column.addStretch()
        
        # 将左右列添加到参数布局
        params_layout.addLayout(outer_left_column)
        params_layout.addLayout(right_column)
        
        # 将参数布局添加到主布局
        main_layout.addLayout(params_layout)
        
        # 输出结果显示区域：放在主布局的最下面，通过滚动条访问
        result_group = QGroupBox("输出结果")
        result_layout = QVBoxLayout(result_group)
        
        # 结果显示文本框
        self._result_text = QTextEdit()
        self._result_text.setReadOnly(True)
        self._result_text.setMinimumHeight(400)  # 输出结果显示框的最小高度
        # 设置自定义上下文菜单策略
        self._result_text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # 连接上下文菜单信号
        self._result_text.customContextMenuRequested.connect(self._on_result_text_context_menu)
        result_layout.addWidget(self._result_text)
        
        # 将结果区域添加到主布局的最下面
        main_layout.addWidget(result_group)
        
        # 设置滚动区域的Widget
        scroll_area.setWidget(scroll_widget)
        
        # 设置主布局
        main_widget_layout = QVBoxLayout(self)
        main_widget_layout.addWidget(scroll_area)
        
        # 为所有QLineEdit控件设置自定义上下文菜单
        for widget in self.findChildren(QLineEdit):
            widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            widget.customContextMenuRequested.connect(self._on_input_context_menu)
        
        # 初始化时根据默认选择的基础样式隐藏/显示相应的输入字段
        # 默认选择的是T型基础，所以需要隐藏基础顶面宽度输入框
        for i in range(self._base_top_width_layout.count()):
            widget = self._base_top_width_layout.itemAt(i).widget()
            if widget:
                widget.hide()
        
    def _connect_signals(self):
        """连接信号和槽"""
        # 连接计算按钮的点击信号
        self._calculate_btn.clicked.connect(self._on_calculate_clicked)
        # 连接导出计算书按钮的点击信号
        self._export_btn.clicked.connect(self._on_export_triggered)
        # 连接导出料表按钮的点击信号
        self._export_material_btn.clicked.connect(self._on_export_material_triggered)
        # 连接基础样式变化信号
        self._foundation_style_combo.currentTextChanged.connect(self._on_foundation_style_changed)
        # 连接管墩形式变化信号
        self._pipe_support_type_combo.currentTextChanged.connect(self._on_pipe_support_type_changed)
    
    @Slot()
    def _on_result_text_context_menu(self, pos):
        """处理输出结果文本框的上下文菜单请求"""
        from PySide6.QtWidgets import QMenu
        
        # 创建上下文菜单
        menu = QMenu(self._result_text)
        
        # 添加复制选项
        copy_action = menu.addAction("复制 (Ctrl+C)")
        copy_action.triggered.connect(self._result_text.copy)
        
        # 添加全选选项
        select_all_action = menu.addAction("全选 (Ctrl+A)")
        select_all_action.triggered.connect(self._result_text.selectAll)
        
        # 显示菜单
        menu.exec_(self._result_text.mapToGlobal(pos))
    
    @Slot()
    def _on_foundation_style_changed(self, style):
        """处理基础样式变化事件"""
        if style == "梯形基础":
            # 基础样式为梯形基础时：
            # 1. 清空底板高度输入框
            self._base_plate_height_edit.clear()
            # 2. 清空基础短柱长度和基础短柱宽度输入框
            self._base_column_length_edit.clear()
            self._base_column_width_edit.clear()
            # 3. 隐藏底板高度输入框及其标签
            for i in range(self._base_plate_height_layout.count()):
                widget = self._base_plate_height_layout.itemAt(i).widget()
                if widget:
                    widget.hide()
            # 4. 隐藏基础短柱长度和基础短柱宽度输入框及其标签
            for i in range(self._base_column_length_layout.count()):
                widget = self._base_column_length_layout.itemAt(i).widget()
                if widget:
                    widget.hide()
            for i in range(self._base_column_width_layout.count()):
                widget = self._base_column_width_layout.itemAt(i).widget()
                if widget:
                    widget.hide()
            # 5. 显示基础顶面宽度输入框及其标签
            for i in range(self._base_top_width_layout.count()):
                widget = self._base_top_width_layout.itemAt(i).widget()
                if widget:
                    widget.show()
        else:
            # 基础样式为T型基础时：
            # 1. 显示底板高度输入框及其标签
            for i in range(self._base_plate_height_layout.count()):
                widget = self._base_plate_height_layout.itemAt(i).widget()
                if widget:
                    widget.show()
            # 2. 显示基础短柱长度和基础短柱宽度输入框及其标签
            for i in range(self._base_column_length_layout.count()):
                widget = self._base_column_length_layout.itemAt(i).widget()
                if widget:
                    widget.show()
            for i in range(self._base_column_width_layout.count()):
                widget = self._base_column_width_layout.itemAt(i).widget()
                if widget:
                    widget.show()
            # 3. 隐藏基础顶面宽度输入框及其标签
            for i in range(self._base_top_width_layout.count()):
                widget = self._base_top_width_layout.itemAt(i).widget()
                if widget:
                    widget.hide()
    
    @Slot()
    def _on_pipe_support_type_changed(self, support_type):
        """处理管墩形式变化事件"""
        # 这里可以添加管墩形式变化的处理逻辑
        pass    
    @Slot()
    def _on_input_context_menu(self, pos):
        """处理输入控件的上下文菜单请求"""
        from PySide6.QtWidgets import QMenu
        
        # 获取发送信号的控件
        sender = self.sender()
        if not sender:
            return
        
        # 创建上下文菜单
        menu = QMenu(sender)
        
        # 添加撤销选项
        undo_action = menu.addAction("撤销 (Ctrl+Z)")
        undo_action.triggered.connect(sender.undo)
        
        # 添加重做选项
        redo_action = menu.addAction("重做 (Ctrl+Y)")
        redo_action.triggered.connect(sender.redo)
        
        menu.addSeparator()
        
        # 添加剪切选项
        cut_action = menu.addAction("剪切 (Ctrl+X)")
        cut_action.triggered.connect(sender.cut)
        
        # 添加复制选项
        copy_action = menu.addAction("复制 (Ctrl+C)")
        copy_action.triggered.connect(sender.copy)
        
        # 添加粘贴选项
        paste_action = menu.addAction("粘贴 (Ctrl+V)")
        paste_action.triggered.connect(sender.paste)
        
        menu.addSeparator()
        
        # 添加删除选项
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(sender.del_)
        
        menu.addSeparator()
        
        # 添加全选选项
        select_all_action = menu.addAction("全选 (Ctrl+A)")
        select_all_action.triggered.connect(sender.selectAll)
        
        # 显示菜单
        menu.exec_(sender.mapToGlobal(pos))
    

    
    @Slot()
    def _on_calculate_clicked(self):
        """计算按钮点击事件"""
        try:
            # 获取输入值并转换为数值类型
            base_length = float(self._base_length_edit.text()) if self._base_length_edit.text() else 0
            base_bottom_width = float(self._base_bottom_width_edit.text()) if self._base_bottom_width_edit.text() else 0
            base_column_length = float(self._base_column_length_edit.text()) if self._base_column_length_edit.text() else 0
            base_column_width = float(self._base_column_width_edit.text()) if self._base_column_width_edit.text() else 0
            base_height = float(self._base_height_edit.text()) if self._base_height_edit.text() else 0
            base_height_above_ground = float(self._base_height_above_ground_edit.text()) if self._base_height_above_ground_edit.text() else 0
            # 计算基底埋深：基础高度减去基础高出地面高度
            depth = base_height - base_height_above_ground
            # 注意：垫层厚度单位已改为mm，需要转换为m
            cushion_thickness = float(self._cushion_thickness_edit.text()) / 1000 if self._cushion_thickness_edit.text() else 0
            replacement_width = float(self._replacement_width_edit.text()) if self._replacement_width_edit.text() else 0
            replacement_thickness = float(self._replacement_thickness_edit.text()) if self._replacement_thickness_edit.text() else 0
            
            # 获取基础个数
            foundation_count = int(self._foundation_count_edit.text()) if self._foundation_count_edit.text() else 1  # 默认1个
            
            # 获取基础形式参数
            foundation_style = self._foundation_style_combo.currentText()
            # 获取底板高度（仅T型基础有效）
            base_plate_height = float(self._base_plate_height_edit.text()) if self._base_plate_height_edit.text() else 0
            # 获取基础顶面宽度（仅梯形基础有效）
            base_top_width = float(self._base_top_width_edit.text()) if self._base_top_width_edit.text() else 0
            # 获取管墩形式
            pipe_support_type = self._pipe_support_type_combo.currentText()
            # 获取地下水考虑选项
            consider_groundwater = self._consider_groundwater_combo.currentText()
            # 计算覆土重度：考虑地下水时为10 KN/m³，否则为18 KN/m³
            soil_density = 10 if consider_groundwater == "是" else 18
            # 获取荷载参数
            upper_vertical_load = float(self._upper_vertical_load_edit.text()) if self._upper_vertical_load_edit.text() else 0
            upper_horizontal_load = float(self._upper_horizontal_load_edit.text()) if self._upper_horizontal_load_edit.text() else 0
            # 获取地基承载力
            bearing_capacity = float(self._bearing_capacity_edit.text()) if self._bearing_capacity_edit.text() else 0
            
            # 调用计算方法（单个基础）
            basic_volume_single = self._logic.calculate_basic_volume(base_length, base_bottom_width, base_top_width, base_height, base_column_length, base_column_width, base_plate_height, foundation_style)
            cushion_volume_single = self._logic.calculate_cushion_volume(base_length, base_bottom_width, cushion_thickness, foundation_style)
            replacement_volume_single = self._logic.calculate_replacement_volume(base_length, base_bottom_width, replacement_width, replacement_thickness, foundation_style)
            
            # 获取预埋钢板参数
            plate_length = float(self._plate_length_edit.text()) if self._plate_length_edit.text() else 0
            plate_width = float(self._plate_width_edit.text()) if self._plate_width_edit.text() else 0
            plate_thickness = float(self._plate_thickness_edit.text()) if self._plate_thickness_edit.text() else 0
            
            # 计算预埋钢板体积（单个基础）
            plate_volume_single = self._logic.calculate_plate_volume(plate_length, plate_width, plate_thickness)
            
            # 计算钢材重量（单个基础）- 仅计算预埋钢板重量
            total_steel_volume_single = plate_volume_single
            steel_weight_kg_single = total_steel_volume_single * 7850  # 钢材密度：7850 kg/m³
            steel_weight_single = steel_weight_kg_single / 1000  # 转换为吨(t)
            
            # 乘以基础个数，得到最终结果
            basic_volume = basic_volume_single * foundation_count
            cushion_volume = cushion_volume_single * foundation_count
            replacement_volume = replacement_volume_single * foundation_count
            steel_weight = steel_weight_single * foundation_count
            steel_weight_kg = steel_weight_kg_single * foundation_count
            plate_volume = plate_volume_single * foundation_count
            
            # 计算基础防腐面积（单个基础）
            anticorrosion_area_single = self._logic.calculate_anticorrosion_area(base_length, base_bottom_width, depth, base_column_length, base_column_width, base_plate_height, foundation_style, base_top_width)
            # 乘以基础个数，得到最终结果
            anticorrosion_area = anticorrosion_area_single * foundation_count
            
            # 验算地基承载力（单个基础）
            bearing_check_result_single = self._logic.check_bearing_capacity(
                upper_vertical_load,
                base_length,
                base_bottom_width,
                base_height,
                bearing_capacity,
                foundation_style,
                base_column_length,
                base_column_width,
                base_plate_height,
                base_height_above_ground,
                upper_horizontal_load,
                consider_groundwater,
                base_top_width
            )
            # 计算总基础的地基承载力验算（对于单个基础，结果相同）
            is_bearing_satisfied, basic_weight, soil_load, total_load, base_pressure, concrete_density, pkmax, pkmin, base_moment, section_modulus = bearing_check_result_single
            
            # 计算基底埋深：基础高度减去基础高出地面高度
            depth = base_height - base_height_above_ground
            # 计算地基承载力修正值
            # 地基承载力修正值 = 地基承载力输入值 + 1 * 计算覆土重度 * (基础高度 - 基础高出地面高度 - 0.5)
            bearing_capacity_corrected = bearing_capacity + 1 * soil_density * (depth - 0.5)
            # 确保修正后的地基承载力不小于原始值
            bearing_capacity_corrected = max(bearing_capacity_corrected, bearing_capacity)
            
            # 计算1.2倍的地基承载力修正值
            bearing_capacity_corrected_12 = 1.2 * bearing_capacity_corrected
            
            # 综合判断地基承载力是否满足要求
            if upper_horizontal_load == 0 or foundation_style != "T型基础":
                # 当水平荷载为0或非T型基础时，只检查地基承载力
                is_bearing_satisfied_final = is_bearing_satisfied
                bearing_check_result = "✅ 满足要求" if is_bearing_satisfied else "❌ 不满足要求（平均压力超过地基承载力）"
            else:
                # 当水平荷载不为0且为T型基础时，检查所有条件
                is_bearing_satisfied_final = is_bearing_satisfied and (pkmax <= bearing_capacity_corrected_12) and (pkmin >= 0)
                # 生成判断结果信息
                bearing_check_result = "✅ 满足要求"
                if not is_bearing_satisfied:
                    bearing_check_result = "❌ 不满足要求（平均压力超过地基承载力）"
                elif pkmax > bearing_capacity_corrected_12:
                    bearing_check_result = "❌ 不满足要求（最大压力超过1.2倍地基承载力修正值）"
                elif pkmin <= 0:
                    bearing_check_result = "⚠️ Pkmin<0，需要验算零应力区"
            
            # 计算抗倾覆（仅梯形基础）
            overturning_check_result = None
            is_overturning_satisfied = False
            resisting_moment = 0
            overturning_moment = 0
            safety_factor = 0
            overturning_total_vertical_load = 0
            arm_length = 0
            if foundation_style != "T型基础":
                # 调用抗倾覆验算方法
                overturning_check_result = self._logic.check_overturning(
                    upper_vertical_load,
                    upper_horizontal_load,
                    base_length,
                    base_bottom_width,
                    base_height,
                    foundation_style,
                    base_column_length,
                    base_column_width,
                    base_plate_height,
                    base_top_width
                )
                # 解包抗倾覆验算结果
                is_overturning_satisfied, resisting_moment, overturning_moment, safety_factor, overturning_total_vertical_load, arm_length = overturning_check_result
            
            # 生成基础体积计算的HTML
            if foundation_style == "T型基础":
                foundation_volume_html = f"""
                        <div class="formula">（一）单个基础体积：</div>
                        <div class="formula">底板体积：{base_length}m × {base_bottom_width}m × {base_plate_height}m</div>
                        <div class="formula">短柱体积：{base_column_length}m × {base_column_width}m × ({base_height}m - {base_plate_height}m)</div>
                        <div class="formula-result">= {basic_volume_single:.3f} m³</div>
                """
            else:
                foundation_volume_html = f"""
                        <div class="formula">（一）单个基础体积：({base_bottom_width}m + {base_top_width}m) × {base_height}m / 2 × {base_length}m</div>
                        <div class="formula-result">= {basic_volume_single:.3f} m³</div>
                """
            
            # 生成垫层体积计算的HTML
            cushion_volume_html = f"""
                        <div class="formula">（一）单个基础垫层体积：({base_length}m + 2×0.1m) × ({base_bottom_width}m + 2×0.1m) × {cushion_thickness}m</div>
                        <div class="formula-result">= {cushion_volume_single:.3f} m³</div>
            """
            
            # 生成换填级配砂石体积计算的HTML
            replacement_volume_html = f"""
                        <div class="formula">（一）单个基础换填级配砂石体积：({base_length}m + 2 × {replacement_width}m) × ({base_bottom_width}m + 2 × {replacement_width}m) × {replacement_thickness}m</div>
                        <div class="formula-result">= {replacement_volume_single:.3f} m³</div>
            """
            
            # 生成基础防腐面积计算的HTML
            if foundation_style == "T型基础":
                anticorrosion_area_html = f"""
                        <div class="formula">（一）单个基础防腐面积</div>
                        <div class="formula">底板侧面积 = ({base_length}m + {base_bottom_width}m) × 2 × {base_plate_height}m</div>
                        <div class="formula">短柱侧面积 = ({base_column_length}m + {base_column_width}m) × 2 × ({depth}m - {base_plate_height}m)</div>
                        <div class="formula">基底埋深 = {depth:.3f}m</div>
                        <div class="formula-result">= {anticorrosion_area_single:.3f} m²</div>
                """
            else:
                import math
                slant_height = math.sqrt(depth ** 2 + ((base_bottom_width - base_top_width) / 2) ** 2)
                anticorrosion_area_html = f"""
                        <div class="formula">（一）单个基础防腐面积</div>
                        <div class="formula">2个梯形侧面面积 = 2 × ({base_top_width}m + {base_bottom_width}m) × {depth}m / 2</div>
                        <div class="formula">2个矩形侧面面积 = 2 × √({depth}m² + (({base_bottom_width}m - {base_top_width}m)/2)²) × {base_length}m</div>
                        <div class="formula">斜边长 = √({depth:.3f}² + {((base_bottom_width - base_top_width)/2):.3f}²) = {slant_height:.3f}m</div>
                        <div class="formula-result">= {anticorrosion_area_single:.3f} m²</div>
                """
            
            # 格式化输出结果为HTML格式
            result_html = f"""<html>
            <head>
                <style>
                    body {{ font-family: 'Microsoft YaHei UI', 'Consolas', 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; }}
                    
                    /* 通用卡片样式 */
                    .card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f5f5f5); border: 1px solid #ccc; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
                    .dark-theme .card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2c2c2c, stop:1 #1e1e1e); border: 1px solid #444; }}
                    
                    /* 标题样式 */
                    h2 {{ color: #3498DB; margin-top: 0; margin-bottom: 15px; font-size: 16px; font-weight: bold; border-bottom: 2px solid #3498DB; padding-bottom: 5px; }}
                    .dark-theme h2 {{ color: #3498DB; border-bottom-color: #3498DB; }}
                    
                    /* 参数表格样式 */
                    .param-table {{ width: 100%; border-collapse: collapse; }}
                    .param-table tr {{ border-bottom: 1px solid #eee; }}
                    .dark-theme .param-table tr {{ border-bottom-color: #333; }}
                    .param-table td {{ padding: 8px 15px; vertical-align: middle; }}
                    
                    /* 参数项样式 */
                    .param-item {{ width: 33.33%; padding: 8px 15px; }}
                    
                    /* 标签和值样式 */
                    .param-label {{ font-weight: bold; color: #555; margin-right: 8px; }}
                    .dark-theme .param-label {{ color: #ffffff; }}
                    .param-value {{ color: #333; }}
                    .dark-theme .param-value {{ color: #ffffff; }}
                    
                    /* 计算结果区样式 */
                    .result-section {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e8f4f8, stop:1 #d4e6f1); border: 1px solid #aed6f1; border-radius: 8px; padding: 20px; margin-bottom: 15px; }}
                    .dark-theme .result-section {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a252f, stop:1 #0f171d); border: 1px solid #3498DB; }}
                    
                    .calculation {{ margin-bottom: 15px; padding: 10px 0; background: transparent; border-radius: 0; }}
                    .dark-theme .calculation {{ background: transparent; }}
                    
                    .formula {{ font-family: 'Consolas', monospace; color: #2c3e50; margin-bottom: 5px; }}
                    .dark-theme .formula {{ color: #ffffff; }}
                    
                    .formula-result {{ font-weight: bold; color: #3498DB; margin-left: 20px; }}
                    .dark-theme .formula-result {{ color: #64b5f6; }}
                    
                    /* 最终结果样式 */
                    .final-results {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef); border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; }}
                    .dark-theme .final-results {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2c3e50, stop:1 #1a2530); border: 1px solid #444; }}
                    
                    .final-table {{ width: 100%; border-collapse: collapse; }}
                    .final-table tr {{ border-bottom: 1px solid #eee; }}
                    .dark-theme .final-table tr {{ border-bottom-color: #333; }}
                    .final-table td {{ padding: 10px 15px; vertical-align: middle; }}
                    .result-label {{ font-weight: bold; color: #333; margin-right: 15px; min-width: 180px; }}
                    .dark-theme .result-label {{ color: #ffffff; }}
                    .result-value {{ font-weight: bold; font-size: 16px; color: #3498DB; }}
                    .dark-theme .result-value {{ color: #64b5f6; }}
                </style>
            </head>
            <body>
                <!-- 最终结果区 -->
                <div class="final-results">
                    <h2>最终计算结果</h2>
                    <table class="final-table">
                        <tr><td class="result-label">基础体积</td><td class="result-value">{basic_volume:.3f} m³</td></tr>
                        <tr><td class="result-label">垫层体积</td><td class="result-value">{cushion_volume:.3f} m³</td></tr>
                        <tr><td class="result-label">换填级配砂石体积</td><td class="result-value">{replacement_volume:.3f} m³</td></tr>
                        <tr><td class="result-label">钢材重量</td><td class="result-value">{steel_weight:.3f} t</td></tr>
                        <tr><td class="result-label">基础防腐面积</td><td class="result-value">{anticorrosion_area:.3f} m²</td></tr>
                        <tr><td class="result-label">地基承载力验算</td><td class="result-value">{bearing_check_result}</td></tr>
                        {('<tr><td class="result-label">抗倾覆验算</td><td class="result-value">' + ('✅ 满足要求' if is_overturning_satisfied else '❌ 不满足要求（安全系数小于1.6）') + '</td></tr>') if foundation_style != "T型基础" and overturning_check_result else ''}
                    </table>
                </div>
                
                <!-- 输入参数区 -->
                <div class="card">
                    <h2>输入参数</h2>
                    <table class="param-table">
                        <tr>
                            <td class="param-item"><span class="param-label">底板长度：</span><span class="param-value">{base_length}m</span></td>
                            <td class="param-item"><span class="param-label">底板宽度：</span><span class="param-value">{base_bottom_width}m</span></td>
                            <td class="param-item"><span class="param-label">基础短柱长度：</span><span class="param-value">{base_column_length}m</span></td>
                        </tr>
                        <tr>
                            <td class="param-item"><span class="param-label">基础短柱宽度：</span><span class="param-value">{base_column_width}m</span></td>
                            <td class="param-item"><span class="param-label">基础顶面宽度：</span><span class="param-value">{base_top_width}m</span></td>
                            <td class="param-item"><span class="param-label">基础高度：</span><span class="param-value">{base_height}m</span></td>
                        </tr>
                        <tr>
                            <td class="param-item"><span class="param-label">基础高出地面高度：</span><span class="param-value">{base_height_above_ground}m</span></td>
                            <td class="param-item"><span class="param-label">基底埋深：</span><span class="param-value">{depth:.3f}m</span></td>
                            <td class="param-item"><span class="param-label">垫层厚度：</span><span class="param-value">{float(self._cushion_thickness_edit.text()) if self._cushion_thickness_edit.text() else 0}mm</span></td>
                        </tr>
                        <tr>
                            <td class="param-item"><span class="param-label">换填厚度：</span><span class="param-value">{replacement_thickness}m</span></td>
                            <td class="param-item"><span class="param-label">换填宽度：</span><span class="param-value">{replacement_width}m</span></td>
                            <td class="param-item"><span class="param-label">基础数量：</span><span class="param-value">{foundation_count}个</span></td>
                        </tr>
                        <tr>
                            <td class="param-item"><span class="param-label">预埋钢板：</span><span class="param-value">{plate_length}m × {plate_width}m × {plate_thickness}mm</span></td>
                            <td class="param-item"><span class="param-label">基础样式：</span><span class="param-value">{foundation_style}</span></td>
                            <td class="param-item"><span class="param-label">管墩形式：</span><span class="param-value">{pipe_support_type}</span></td>
                        </tr>                        <tr>
                            <td class="param-item"><span class="param-label">是否考虑地下水：</span><span class="param-value">{consider_groundwater}</span></td>
                            <td class="param-item"><span class="param-label">上部垂直荷载：</span><span class="param-value">{upper_vertical_load}KN</span></td>
                            <td class="param-item"><span class="param-label">上部水平荷载：</span><span class="param-value">{upper_horizontal_load}KN</span></td>
                        </tr>                        <tr>
                            <td class="param-item"><span class="param-label">地基承载力：</span><span class="param-value">{bearing_capacity}kPa</span></td>
                        </tr>                    </table>
                </div>
                
                <!-- 计算结果区 -->
                <div class="result-section">
                    <h2>计算过程</h2>
                    
                    <div class="calculation">
                        <div class="formula">一、基础体积计算</div>
                        {foundation_volume_html}
                        <div class="formula">（二）总基础体积：{basic_volume_single:.3f}m³ × {foundation_count}个</div>
                        <div class="formula-result">= {basic_volume:.3f} m³</div>
                    </div>
                    
                    <div class="calculation">
                        <div class="formula">二、垫层体积计算</div>
                        {cushion_volume_html}
                        <div class="formula">（二）总垫层体积：{cushion_volume_single:.3f}m³ × {foundation_count}个</div>
                        <div class="formula-result">= {cushion_volume:.3f} m³</div>
                    </div>
                    
                    <div class="calculation">
                        <div class="formula">三、换填级配砂石体积计算</div>
                        {replacement_volume_html}
                        <div class="formula">（二）总换填级配砂石体积：{replacement_volume_single:.3f}m³ × {foundation_count}个</div>
                        <div class="formula-result">= {replacement_volume:.3f} m³</div>
                    </div>
                    
                    <div class="calculation">
                        <div class="formula">四、预埋钢板体积计算</div>
                        <div class="formula">（一）单个预埋钢板体积：{plate_length}m × {plate_width}m × {plate_thickness}mm</div>
                        <div class="formula">= {plate_length}m × {plate_width}m × {plate_thickness/1000:.3f}m</div>
                        <div class="formula-result">= {plate_volume_single:.3f} m³</div>
                        <div class="formula">（二）总预埋钢板体积：{plate_volume_single:.3f}m³ × {foundation_count}个</div>
                        <div class="formula-result">= {plate_volume:.3f} m³</div>
                    </div>
                    
                    <div class="calculation">
                        <div class="formula">五、钢材重量计算</div>
                        <div class="formula">（一）单个基础钢材重量：{plate_volume_single:.3f}m³ × 7850kg/m³</div>
                        <div class="formula-result">= {steel_weight_kg_single:.3f} kg</div>
                        <div class="formula-result">= {steel_weight_single:.3f} t</div>
                        <div class="formula">（二）总钢材重量：{steel_weight_kg_single:.3f}kg × {foundation_count}个</div>
                        <div class="formula-result">= {steel_weight_kg:.3f} kg</div>
                        <div class="formula-result">= {steel_weight:.3f} t</div>
                    </div>
                    
                    <div class="calculation">
                        <div class="formula">六、基础防腐面积计算</div>
                        {anticorrosion_area_html}
                        <div class="formula">（二）总基础防腐面积：{anticorrosion_area_single:.3f}m² × {foundation_count}个</div>
                        <div class="formula-result">= {anticorrosion_area:.3f} m²</div>
                    </div>
                    
                    <div class="calculation">
                        <div class="formula">七、地基承载力验算</div>
                        <div class="formula">（一）基础体积：</div>
                        <div class="formula">
                            {f'底板体积：{base_length}m × {base_bottom_width}m × {base_plate_height}m = {base_length * base_bottom_width * base_plate_height:.3f} m³<br>短柱体积：{base_column_length}m × {base_column_width}m × ({base_height}m - {base_plate_height}m) = {base_column_length * base_column_width * (base_height - base_plate_height):.3f} m³<br>总体积：{base_length * base_bottom_width * base_plate_height:.3f}m³ + {base_column_length * base_column_width * (base_height - base_plate_height):.3f}m³ = {base_length * base_bottom_width * base_plate_height + base_column_length * base_column_width * (base_height - base_plate_height):.3f} m³' if foundation_style == "T型基础" else f'({base_bottom_width}m + {base_top_width}m) × {base_height}m / 2 × {base_length}m = {basic_volume_single:.3f} m³'}
                        </div>
                        <div class="formula">（二）基础自重：{basic_volume_single:.3f}m³ × {concrete_density}KN/m³ = {basic_weight:.3f} KN</div>
                        {f'''
                        <div class="formula">（三）覆土荷载：{soil_density}kN/m³ × ({base_length * base_bottom_width:.3f}m² - {base_column_length * base_column_width:.3f}m²) × ({base_height:.3f}m - {base_height_above_ground:.3f}m - {base_plate_height:.3f}m) = {soil_load:.3f} KN</div>
                        <div class="formula">（四）总荷载：上部荷载 {upper_vertical_load}KN + 基础自重 {basic_weight:.3f}KN + 覆土荷载 {soil_load:.3f}KN = {total_load:.3f} KN</div>
                        <div class="formula">（五）基底面积：{base_length}m × {base_bottom_width}m = {base_length * base_bottom_width:.3f} m²</div>
                        <div class="formula">（六）基底压力：{total_load:.3f}KN ÷ {base_length * base_bottom_width:.3f}m² = {base_pressure:.3f} kPa</div>
                        <div class="formula">（七）地基承载力：{bearing_capacity} kPa</div>
                        <div class="formula">（八）验算结果：{'✅ 地基承载力满足要求' if is_bearing_satisfied else '❌ 地基承载力不满足要求'}</div>
                        ''' if foundation_style == "T型基础" and soil_load > 0 else f'''
                        <div class="formula">（三）总荷载：上部荷载 {upper_vertical_load}KN + 基础自重 {basic_weight:.3f}KN = {total_load:.3f} KN</div>
                        <div class="formula">（四）基底面积：{base_length}m × {base_bottom_width}m = {base_length * base_bottom_width:.3f} m²</div>
                        <div class="formula">（五）基底压力：{total_load:.3f}KN ÷ {base_length * base_bottom_width:.3f}m² = {base_pressure:.3f} kPa</div>
                        <div class="formula">（六）地基承载力：{bearing_capacity} kPa</div>
                        <div class="formula">（七）验算结果：{'✅ 地基承载力满足要求' if is_bearing_satisfied else '❌ 地基承载力不满足要求'}</div>
                        '''}
                        
                        {f'''
                        <div class="formula">（九）基底弯矩计算：</div>
                        <div class="formula">水平荷载：{upper_horizontal_load} KN</div>
                        <div class="formula">作用高度：{base_height} m</div>
                        <div class="formula">基底弯矩 Mk = {upper_horizontal_load}KN × {base_height}m = {base_moment:.3f} kN·m</div>
                        <div class="formula">（十）截面抵抗矩计算：</div>
                        <div class="formula">底板长度：{base_length} m</div>
                        <div class="formula">底板宽度：{base_bottom_width} m</div>
                        <div class="formula">较长边尺寸：{max(base_length, base_bottom_width):.3f} m</div>
                        <div class="formula">较短边尺寸：{min(base_length, base_bottom_width):.3f} m</div>
                        <div class="formula">截面抵抗矩 W = ({min(base_length, base_bottom_width):.3f}m × {max(base_length, base_bottom_width):.3f}m²) / 6 = {section_modulus:.3f} m³</div>
                        <div class="formula">（十一）基底压力计算：</div>
                        <div class="formula">Pkmax = {total_load:.3f}/ {base_length * base_bottom_width:.3f} + {base_moment:.3f}/ {section_modulus:.3f}= {pkmax:.3f} kPa</div>
                        <div class="formula">Pkmin = {total_load:.3f}/ {base_length * base_bottom_width:.3f} - {base_moment:.3f}/ {section_modulus:.3f}= {pkmin:.3f} kPa</div>
                        
                        <div class="formula">（十二）地基承载力修正：</div>
                        <div class="formula">基底埋深：{depth:.3f} m</div>
                        <div class="formula">计算覆土重度：{soil_density} kN/m³</div>
                        <div class="formula">地基承载力修正值 = {bearing_capacity}kPa + 1 × {soil_density}kN/m³ × ({depth:.3f}m - 0.5m) = {bearing_capacity_corrected:.3f} kPa</div>
                        <div class="formula">1.2 × 地基承载力修正值 = 1.2 × {bearing_capacity_corrected:.3f}kPa = {bearing_capacity_corrected_12:.3f} kPa</div>
                        <div class="formula">（十三）最终验算：</div>
                        <div class="formula">Pkmax = {pkmax:.3f} kPa {'≤' if pkmax <= bearing_capacity_corrected_12 else '>'} {bearing_capacity_corrected_12:.3f} kPa</div>
                        <div class="formula">Pkmin = {pkmin:.3f} kPa {'>' if pkmin > 0 else '≤'} 0 kPa</div>
                        ''' if foundation_style == "T型基础" and upper_horizontal_load > 0 else ''}
                        <div class="formula">最终结果：{bearing_check_result}</div>
                        
                        # 仅在梯形基础时显示抗倾覆计算
                        {f'''
                        <div class="calculation">
                            <div class="formula">八、抗倾覆验算</div>
                            <div class="formula">（一）基础体积：{basic_volume_single:.3f} m³</div>
                            <div class="formula">（二）基础自重：{basic_volume_single:.3f}m³ × {concrete_density}KN/m³ = {basic_weight:.3f} KN</div>
                            <div class="formula">（三）总垂直荷载：上部荷载 {upper_vertical_load}KN + 基础自重 {basic_weight:.3f}KN = {overturning_total_vertical_load:.3f} KN</div>
                            <div class="formula">（四）倾覆力矩：水平荷载 {upper_horizontal_load}KN × 作用高度 {base_height}m = {overturning_moment:.3f} kN·m</div>
                            <div class="formula">（五）抗倾覆力矩：总垂直荷载 {overturning_total_vertical_load:.3f}KN × 力臂 {arm_length:.3f}m = {resisting_moment:.3f} kN·m</div>
                            <div class="formula">（六）抗倾覆安全系数：{resisting_moment:.3f}kN·m / {overturning_moment:.3f}kN·m = {safety_factor:.3f}</div>
                            <div class="formula">（七）抗倾覆验算结果：{'✅ 满足要求' if is_overturning_satisfied else '❌ 不满足要求（安全系数小于1.6）'}</div>
                        </div>
                        ''' if foundation_style != "T型基础" and overturning_check_result else ''}
                    </div>            </body>
            </html>"""            
            # 设置HTML结果
            self._result_text.setHtml(result_html)
        
        except ValueError as e:
            # 处理输入值转换错误
            error_html = f"""<html>
            <head>
                <style>
                    body {{ font-family: 'Microsoft YaHei UI', 'Consolas', 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; }}
                    .error-card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffebee, stop:1 #ffcdd2); border: 1px solid #f44336; border-radius: 8px; padding: 20px; margin: 15px; }}
                    .error-title {{ color: #f44336; font-size: 16px; font-weight: bold; margin-bottom: 10px; }}
                    .error-message {{ color: #c62828; margin-bottom: 8px; }}
                    .error-detail {{ color: #8e0000; font-family: 'Consolas', monospace; }}
                </style>
            </head>
            <body>
                <div class="error-card">
                    <div class="error-title">计算错误</div>
                    <div class="error-message">请确保所有输入值为有效的数值。</div>
                    <div class="error-detail">错误详情：{str(e)}</div>
                </div>
            </body>
            </html>"""
        except ZeroDivisionError:
            # 处理除零错误
            error_html = f"""<html>
            <head>
                <style>
                    body {{ font-family: 'Microsoft YaHei UI', 'Consolas', 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; }}
                    .error-card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffebee, stop:1 #ffcdd2); border: 1px solid #f44336; border-radius: 8px; padding: 20px; margin: 15px; }}
                    .error-title {{ color: #f44336; font-size: 16px; font-weight: bold; margin-bottom: 10px; }}
                    .error-message {{ color: #c62828; margin-bottom: 8px; }}
                    .error-detail {{ color: #8e0000; font-family: 'Consolas', monospace; }}
                </style>
            </head>
            <body>
                <div class="error-card">
                    <div class="error-title">计算错误</div>
                    <div class="error-message">基底面积为零，无法进行地基承载力验算。</div>
                    <div class="error-detail">错误详情：除数不能为零</div>
                </div>
            </body>
            </html>"""
            self._result_text.setHtml(error_html)
        except Exception as e:
            # 处理其他计算错误
            # 将常见英文错误信息转换为中文
            error_message = str(e)
            if "division by zero" in error_message:
                error_message = "除零错误：请检查输入的参数是否为零"
            elif "float division by zero" in error_message:
                error_message = "浮点除零错误：请检查输入的参数是否为零"
            
            error_html = f"""<html>
            <head>
                <style>
                    body {{ font-family: 'Microsoft YaHei UI', 'Consolas', 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; }}
                    .error-card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffebee, stop:1 #ffcdd2); border: 1px solid #f44336; border-radius: 8px; padding: 20px; margin: 15px; }}
                    .error-title {{ color: #f44336; font-size: 16px; font-weight: bold; margin-bottom: 10px; }}
                    .error-message {{ color: #c62828; }}
                    .error-detail {{ color: #8e0000; font-family: 'Consolas', monospace; margin-top: 8px; }}
                </style>
            </head>
            <body>
                <div class="error-card">
                    <div class="error-title">计算错误</div>
                    <div class="error-message">计算过程中发生了未知错误。</div>
                    <div class="error-detail">错误详情：{error_message}</div>
                </div>
            </body>
            </html>"""
            self._result_text.setHtml(error_html)
    
    @Slot()
    def _on_export_triggered(self):
        """导出计算书按钮点击事件"""
        # 这里可以添加导出计算书的逻辑
        pass
    
    @Slot()
    def _on_export_material_triggered(self):
        """导出料表按钮点击事件"""
        # 这里可以添加导出料表的逻辑
        pass
    
    def reset(self):
        """重置插件UI到初始状态"""
        # 清空所有输入框
        self._base_length_edit.clear()
        self._base_bottom_width_edit.clear()
        self._base_column_length_edit.clear()
        self._base_column_width_edit.clear()
        self._base_top_width_edit.clear()
        self._base_height_edit.clear()
        self._base_height_above_ground_edit.clear()
        self._cushion_thickness_edit.clear()
        self._plate_length_edit.clear()
        self._plate_width_edit.clear()
        self._plate_thickness_edit.clear()
        self._replacement_thickness_edit.clear()
        self._replacement_width_edit.clear()
        self._foundation_count_edit.clear()
        self._base_plate_height_edit.clear()
        self._upper_vertical_load_edit.clear()
        self._upper_horizontal_load_edit.clear()
        self._bearing_capacity_edit.clear()
        # 清空结果文本框
        self._result_text.clear()
        # 重置基础样式为T型基础
        self._foundation_style_combo.setCurrentText("T型基础")
        # 重置管墩形式为固定墩
        self._pipe_support_type_combo.setCurrentText("固定墩")
    
    def save(self, file_path):
        """保存参数到文件
        
        Args:
            file_path: 文件路径
        """
        import json
        
        # 收集所有输入参数
        params = {
            "base_length": self._base_length_edit.text(),
            "base_bottom_width": self._base_bottom_width_edit.text(),
            "base_column_length": self._base_column_length_edit.text(),
            "base_column_width": self._base_column_width_edit.text(),
            "base_top_width": self._base_top_width_edit.text(),
            "base_height": self._base_height_edit.text(),
            "base_height_above_ground": self._base_height_above_ground_edit.text(),
            "cushion_thickness": self._cushion_thickness_edit.text(),
            "plate_length": self._plate_length_edit.text(),
            "plate_width": self._plate_width_edit.text(),
            "plate_thickness": self._plate_thickness_edit.text(),
            "replacement_thickness": self._replacement_thickness_edit.text(),
            "replacement_width": self._replacement_width_edit.text(),
            "foundation_count": self._foundation_count_edit.text(),
            "base_plate_height": self._base_plate_height_edit.text(),
            "upper_vertical_load": self._upper_vertical_load_edit.text(),
            "upper_horizontal_load": self._upper_horizontal_load_edit.text(),
            "bearing_capacity": self._bearing_capacity_edit.text(),
            "foundation_style": self._foundation_style_combo.currentText(),
            "pipe_support_type": self._pipe_support_type_combo.currentText()
        }
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False, indent=2)
    
    def open(self, file_path):
        """从文件加载参数
        
        Args:
            file_path: 文件路径
        """
        import json
        
        try:
            # 从文件加载参数
            with open(file_path, 'r', encoding='utf-8') as f:
                params = json.load(f)
            
            # 设置输入参数
            self._base_length_edit.setText(params.get("base_length", ""))
            self._base_bottom_width_edit.setText(params.get("base_bottom_width", ""))
            self._base_column_length_edit.setText(params.get("base_column_length", ""))
            self._base_column_width_edit.setText(params.get("base_column_width", ""))
            self._base_top_width_edit.setText(params.get("base_top_width", ""))
            self._base_height_edit.setText(params.get("base_height", ""))
            self._base_height_above_ground_edit.setText(params.get("base_height_above_ground", ""))
            self._cushion_thickness_edit.setText(params.get("cushion_thickness", ""))
            self._plate_length_edit.setText(params.get("plate_length", ""))
            self._plate_width_edit.setText(params.get("plate_width", ""))
            self._plate_thickness_edit.setText(params.get("plate_thickness", ""))
            self._replacement_thickness_edit.setText(params.get("replacement_thickness", ""))
            self._replacement_width_edit.setText(params.get("replacement_width", ""))
            self._foundation_count_edit.setText(params.get("foundation_count", ""))
            self._base_plate_height_edit.setText(params.get("base_plate_height", ""))
            self._upper_vertical_load_edit.setText(params.get("upper_vertical_load", ""))
            self._upper_horizontal_load_edit.setText(params.get("upper_horizontal_load", ""))
            self._bearing_capacity_edit.setText(params.get("bearing_capacity", ""))
            
            # 设置基础样式
            foundation_style = params.get("foundation_style", "T型基础")
            self._foundation_style_combo.setCurrentText(foundation_style)
            
            # 设置管墩形式
            pipe_support_type = params.get("pipe_support_type", "固定墩")
            self._pipe_support_type_combo.setCurrentText(pipe_support_type)
            
            # 清空结果文本框
            self._result_text.clear()
            
        except Exception as e:
            # 处理加载错误
            error_html = f"""<html>
            <head>
                <style>
                    body {{ font-family: 'Microsoft YaHei UI', 'Consolas', 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; }}
                    .error-card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffebee, stop:1 #ffcdd2); border: 1px solid #f44336; border-radius: 8px; padding: 20px; margin: 15px; }}
                    .error-title {{ color: #f44336; font-size: 16px; font-weight: bold; margin-bottom: 10px; }}
                    .error-message {{ color: #c62828; }}
                    .error-detail {{ color: #8e0000; font-family: 'Consolas', monospace; margin-top: 8px; }}
                </style>
            </head>
            <body>
                <div class="error-card">
                    <div class="error-title">加载错误</div>
                    <div class="error-message">无法加载文件：{file_path}</div>
                    <div class="error-detail">错误详情：{str(e)}</div>
                </div>
            </body>
            </html>"""
            self._result_text.setHtml(error_html)