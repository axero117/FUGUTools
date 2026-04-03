"""主窗口逻辑"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTabWidget, QMenuBar, QMenu, QToolBar,
                               QStatusBar, QLabel, QStyle, QStyledItemDelegate,
                               QTreeWidget, QTreeWidgetItem)
from PySide6.QtGui import QAction, QActionGroup, QCursor, QColor, QPainter, QPen
from PySide6.QtCore import Qt, QSize

from core.logger import Logger
from core.plugin_manager import PluginManager
from ui.dialogs.about_dialog import AboutDialog
from ui.dialogs.release_notes_dialog import ReleaseNotesDialog


class NavigationItemDelegate(QStyledItemDelegate):
    """侧栏树节点自定义绘制：强化母子层级、状态色与结构提示。"""

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        is_group = index.model().hasChildren(index)
        size.setHeight(42 if is_group else 36)
        return size

    def paint(self, painter: QPainter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        tree_widget = option.widget
        is_group = index.model().hasChildren(index)
        is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        is_hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)

        card_rect = option.rect.adjusted(8, 3, -8, -3)
        if not is_group:
            # 子项额外右缩进，拉开层级
            card_rect.adjust(10, 0, 0, 0)

        # 颜色体系
        if is_group:
            bg = QColor("#E2E8F0")
            border = QColor("#CFD7E2")
            text_color = QColor("#1F2D3D")
            if is_hovered:
                bg = QColor("#E9EEF4")
            if is_selected:
                bg = QColor("#2F80C1")
                border = QColor("#2F80C1")
                text_color = QColor("#FFFFFF")
        else:
            bg = QColor("#F5F6F8")
            border = QColor("#D9DDE3")
            text_color = QColor("#2F3542")
            if is_hovered:
                bg = QColor("#FBFCFD")
            if is_selected:
                bg = QColor("#EAF4FF")
                border = QColor("#BDD9F6")
                text_color = QColor("#1F4E79")

        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(card_rect, 6, 6)

        # 左侧强调条
        if is_group:
            accent_color = QColor("#4A90E2") if not is_selected else QColor(
                "#FFFFFF")
            painter.setPen(Qt.NoPen)
            painter.setBrush(accent_color)
            painter.drawRoundedRect(card_rect.left(), card_rect.top(), 4,
                                    card_rect.height(), 2, 2)
        elif is_selected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#4A90E2"))
            painter.drawRoundedRect(card_rect.left(), card_rect.top(), 3,
                                    card_rect.height(), 1, 1)

        # 文本与结构提示
        text = index.data(Qt.DisplayRole) or ""
        font = option.font
        if is_group:
            font.setBold(True)
            font.setPointSize(10)
            text_rect = card_rect.adjusted(14, 0, -24, 0)
        else:
            font.setBold(False)
            font.setPointSize(9)
            # 子项小圆点（约 12px）
            dot_rect = card_rect.adjusted(10, 0, 0, 0)
            dot_size = 6
            dot_x = dot_rect.left()
            dot_y = dot_rect.center().y() - dot_size // 2
            painter.setPen(QPen(QColor("#9AA7B8"), 1))
            painter.setBrush(
                QColor("#DCE4EE") if not is_selected else QColor("#4A90E2"))
            painter.drawEllipse(dot_x, dot_y, dot_size, dot_size)
            text_rect = card_rect.adjusted(24, 0, -10, 0)

        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)

        # 母节点右侧折叠箭头
        if is_group and isinstance(tree_widget, QTreeWidget):
            item = tree_widget.itemFromIndex(index)
            arrow = "▾" if item and item.isExpanded() else "▸"
            arrow_rect = card_rect.adjusted(0, 0, -8, 0)
            painter.drawText(arrow_rect, Qt.AlignVCenter | Qt.AlignRight,
                             arrow)

        painter.restore()


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()

        self._logger = Logger()
        self._app_instance = None  # 应用实例引用
        self._plugin_manager = None  # 插件管理器引用
        # 插件映射：存储插件名称到工厂函数的映射，工厂函数返回插件UI组件的新实例
        self._plugin_factories = {}
        # 已注册的插件列表
        self._registered_plugins = []

        # 设置窗口属性
        self.setWindowTitle("符构工具箱")
        self.resize(1024, 768)

        # 初始化UI组件
        self._init_ui()

    def _init_ui(self):
        """初始化UI组件"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.centralWidget().setAcceptDrops(True)

        # 主布局：水平布局，左侧工具导航，右侧工作区
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧工具导航（侧边栏）
        self._tool_navigation = QTreeWidget()
        self._tool_navigation.setFixedWidth(210)
        self._tool_navigation.setObjectName("toolNavigation")
        self._tool_navigation.setHeaderHidden(True)
        self._tool_navigation.setRootIsDecorated(False)
        self._tool_navigation.setIndentation(16)
        self._tool_navigation.setUniformRowHeights(True)
        self._tool_navigation.setExpandsOnDoubleClick(False)
        self._tool_navigation.setMouseTracking(True)
        self._tool_navigation.setItemDelegate(
            NavigationItemDelegate(self._tool_navigation))

        # 添加工具项
        # 方案计算（带有子节点，用于显示块式基础计算）
        self._calculation_item = QTreeWidgetItem(self._tool_navigation,
                                                 ["方案计算"])
        self._configure_navigation_item(self._calculation_item, is_group=True)
        # 默认折叠显示
        self._tool_navigation.collapseItem(self._calculation_item)

        # 小工具（带有子节点，用于显示各种小工具）
        self._small_tools_item = QTreeWidgetItem(self._tool_navigation,
                                                 ["小工具"])
        self._configure_navigation_item(self._small_tools_item, is_group=True)
        # 默认折叠显示
        self._tool_navigation.collapseItem(self._small_tools_item)

        # 材料库
        self._material_library_item = QTreeWidgetItem(self._tool_navigation,
                                                      ["材料库"])
        self._configure_navigation_item(self._material_library_item,
                                        is_group=True)
        # 默认折叠显示
        self._tool_navigation.collapseItem(self._material_library_item)

        # 默认不选中任何项，避免初始视觉层级干扰
        self._tool_navigation.clearSelection()

        # 连接节点单击信号，用于展开/折叠分类节点
        self._tool_navigation.itemClicked.connect(self._on_tool_item_clicked)
        # 连接节点双击信号，用于新建标签页
        self._tool_navigation.itemDoubleClicked.connect(
            self._on_tool_double_clicked)

        main_layout.addWidget(self._tool_navigation)

        # 右侧工作区
        self._workspace = QTabWidget()
        self._workspace.setTabsClosable(False)
        self._workspace.setMovable(True)
        self._workspace.setObjectName("workspace")

        # 只设置tabBar的上下文菜单策略并连接信号
        tab_bar = self._workspace.tabBar()
        tab_bar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(
            self._on_tab_bar_context_menu)

        # 添加默认的欢迎页面
        self._add_welcome_tab()

        # 标签切换时同步更新状态栏左侧文本
        self._workspace.currentChanged.connect(
            self._update_status_label_by_tab)

        main_layout.addWidget(self._workspace)

        # 初始化菜单栏
        self._init_menu_bar()

        # 初始化状态栏
        self._init_status_bar()

        # 启用工作区的拖放功能
        self._workspace.setAcceptDrops(True)

        #设置标签栏接受拖放
        tab_bar = self._workspace.tabBar()
        tab_bar.setAcceptDrops(True)

    def _add_welcome_tab(self):
        """添加欢迎页面"""
        welcome_widget = QWidget()
        welcome_widget.setObjectName("welcomeWidget")
        welcome_layout = QVBoxLayout(welcome_widget)
        welcome_layout.setContentsMargins(50, 50, 50, 50)
        welcome_layout.setAlignment(Qt.AlignCenter)
        welcome_layout.setSpacing(25)

        # 欢迎图标
        welcome_icon = QLabel("F U G O")
        welcome_icon.setObjectName("welcomeIcon")
        welcome_icon.setStyleSheet("font-size: 60px;")
        welcome_icon.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_icon)

        # 欢迎标题
        welcome_title = QLabel("欢迎使用符构工具箱！")
        welcome_title.setObjectName("welcomeTitle")
        welcome_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_title)

        # 优雅分隔线
        separator = QWidget()
        separator.setObjectName("welcomeSeparator")
        separator.setFixedHeight(2)
        separator.setMaximumWidth(300)
        welcome_layout.addWidget(separator, 0, Qt.AlignCenter)

        # 欢迎提示
        welcome_tip = QLabel("✨ 点击左侧工具开始计算")
        welcome_tip.setObjectName("welcomeTip")
        welcome_tip.setStyleSheet("font-size: 17px;")
        welcome_tip.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_tip)

        # 添加额外的提示信息
        additional_tip = QLabel("📋 双击工具名称打开新标签页")
        additional_tip.setObjectName("additionalTip")
        additional_tip.setStyleSheet("font-size: 15px;")
        additional_tip.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(additional_tip)

        # 添加底部版权信息
        footer_label = QLabel("© 始于2026")
        footer_label.setObjectName("footerLabel")
        footer_label.setStyleSheet("font-size: 14px; margin-top: 30px;")
        footer_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(footer_label)

        # 将欢迎页面添加到工作区
        self._workspace.addTab(welcome_widget, "欢迎")

    def _init_menu_bar(self):
        """初始化菜单栏"""
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件")

        # 新建动作
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._on_file_new_triggered)
        file_menu.addAction(new_action)

        # 打开动作
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_open_triggered)
        file_menu.addAction(open_action)

        # 保存动作
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._on_save_triggered)
        file_menu.addAction(save_action)

        # 关闭全部标签页动作
        close_all_tabs_action = QAction("关闭全部标签页", self)
        close_all_tabs_action.setShortcut("Ctrl+Shift+W")
        close_all_tabs_action.triggered.connect(self.clear_plugin_tabs)
        file_menu.addAction(close_all_tabs_action)

        file_menu.addSeparator()

        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")

        # 关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._on_about_triggered)
        help_menu.addAction(about_action)

        # 更新说明动作
        release_notes_action = QAction("更新说明", self)
        release_notes_action.triggered.connect(self._on_release_notes_triggered)
        help_menu.addAction(release_notes_action)

        # 帮助文档
        docs_action = QAction("帮助文档", self)
        help_menu.addAction(docs_action)

    def _on_release_notes_triggered(self):
        """显示更新说明对话框"""
        dialog = ReleaseNotesDialog(self)
        dialog.exec()

    def _init_status_bar(self):
        """初始化状态栏"""
        status_bar = QStatusBar()
        status_bar.setObjectName("statusBar")
        self.setStatusBar(status_bar)

        # 左侧：就绪状态
        self._status_label = QLabel("就绪")
        status_bar.addWidget(self._status_label)

        # 中间：拉伸空间
        status_bar.addPermanentWidget(QWidget(), 1)

        # 右侧：版本信息
        version_label = QLabel(" | 版本 v1.0.1")
        status_bar.addPermanentWidget(version_label)

        self._update_status_label_by_tab()

    def _update_status_label_by_tab(self):
        """将状态栏左侧文本更新为当前选中的标签页名称。"""
        if not hasattr(self, "_status_label"):
            return
        if not hasattr(self, "_workspace") or self._workspace.count() == 0:
            self._status_label.setText("就绪")
            return

        current_index = self._workspace.currentIndex()
        if current_index < 0:
            self._status_label.setText("就绪")
            return

        current_tab_text = self._workspace.tabText(current_index).strip()
        self._status_label.setText(current_tab_text or "就绪")

    def set_plugin_manager(self, plugin_manager: PluginManager):
        """设置插件管理器引用
        
        Args:
            plugin_manager: PluginManager实例
        """
        self._plugin_manager = plugin_manager

    def register_plugin(self, plugin_name: str):
        """注册插件到主窗口
        
        Args:
            plugin_name: 插件名称
        """
        if plugin_name in self._registered_plugins:
            return

        # 将插件添加到已注册列表
        self._registered_plugins.append(plugin_name)

        # 确定插件应该添加到哪个分类下
        parent_item = None
        if plugin_name == "YJK柱脚内力处理工具":
            # 将YJK柱脚内力处理工具添加到"小工具"分类下
            parent_item = self._small_tools_item
        elif plugin_name == "型钢特性表":
            # 将型钢特性表添加到"材料库"分类下
            # 查找材料库节点
            for i in range(self._tool_navigation.topLevelItemCount()):
                item = self._tool_navigation.topLevelItem(i)
                if item.text(0) == "材料库":
                    parent_item = item
                    break

        if not parent_item:
            # 默认添加到"方案计算"分类下
            parent_item = self._calculation_item

        # 将插件添加到对应的分类下作为子节点
        plugin_item = QTreeWidgetItem(parent_item, [plugin_name])
        self._configure_navigation_item(plugin_item, is_group=False)
        # 设置子节点样式
        plugin_item.setFlags(plugin_item.flags() | Qt.ItemIsSelectable
                             | Qt.ItemIsEnabled)

        # 存储插件工厂函数，使用插件管理器实例化插件
        self._plugin_factories[
            plugin_name] = lambda name=plugin_name: self._create_plugin_widget(
                name)

    def remove_plugin_tab(self, index: int):
        """移除插件标签页
        
        Args:
            index: 标签页索引
        """
        self._workspace.removeTab(index)

    def clear_plugin_tabs(self):
        """清除所有插件标签页"""
        # 清除所有标签页
        self._workspace.clear()
        # 添加欢迎页面
        self._add_welcome_tab()
        self._update_status_label_by_tab()

    def _on_tool_item_clicked(self, item, column):
        """处理工具导航项单击事件
        
        Args:
            item: 被点击的树节点
            column: 被点击的列
        """
        item_text = item.text(column)

        # 如果点击的是可展开/折叠的分类节点，切换其展开/折叠状态
        if item_text in ["方案计算", "小工具", "材料库"]:
            # 使用QTreeWidgetItem的isExpanded方法检查展开状态
            if item.isExpanded():
                self._tool_navigation.collapseItem(item)
            else:
                self._tool_navigation.expandItem(item)

        # 刷新箭头与状态绘制
        self._tool_navigation.viewport().update()

    def _configure_navigation_item(self, item: QTreeWidgetItem,
                                   is_group: bool):
        """为导航项附加类型属性与基础尺寸，便于样式区分。"""
        item.setData(0, Qt.UserRole, "group" if is_group else "child")
        item.setSizeHint(0, QSize(0, 42 if is_group else 36))

        font = item.font(0)
        font.setBold(is_group)
        item.setFont(0, font)

    def _create_plugin_widget(self, plugin_name: str):
        """创建插件Widget
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            QWidget: 插件的UI组件
        """
        if self._plugin_manager is None:
            return None

        # 使用插件管理器实例化插件
        plugin = self._plugin_manager.get_plugin(plugin_name)
        if plugin is None:
            return None

        # 获取插件的Widget
        widget = plugin.get_widget()

        # 如果型钢特性表插件，连接标题变化信号
        if plugin_name == "型钢特性表" and hasattr(widget, 'title_changed'):
            widget.title_changed.connect(
                lambda title, w=widget: self._update_tab_title(w, title))

        return widget

    def _on_tool_double_clicked(self, item, column):
        """处理工具导航项双击事件
        
        Args:
            item: 被点击的树节点
            column: 被点击的列
        """
        item_text = item.text(column)

        # 检查是否是插件节点
        if item_text in self._plugin_factories:
            # 每次点击都新建一个插件实例
            widget_factory = self._plugin_factories[item_text]
            new_widget = widget_factory()
            if new_widget is None:
                return

            # 添加到工作区
            self._workspace.addTab(new_widget, item_text)
            # 切换到新添加的标签页
            self._workspace.setCurrentIndex(self._workspace.count() - 1)
            self._update_status_label_by_tab()

            # 关闭欢迎标签页
            self._close_welcome_tab()

    def _on_workspace_context_menu(self, pos):
        """处理工作区的上下文菜单请求
        
        Args:
            pos: 上下文菜单请求的位置
        """
        # 获取tabBar
        tab_bar = self._workspace.tabBar()
        if tab_bar is None:
            return

        # 将工作区的位置转换为全局位置
        global_pos = self._workspace.mapToGlobal(pos)
        # 将全局位置转换为tabBar的本地位置
        tab_bar_pos = tab_bar.mapFromGlobal(global_pos)
        # 获取当前右键点击的标签页索引
        index = tab_bar.tabAt(tab_bar_pos)
        if index == -1:  # 没有点击到标签页
            return

        # 创建上下文菜单
        from PySide6.QtWidgets import QMenu
        menu = QMenu(tab_bar)

        # 重新加载选项，添加图标
        reload_action = QAction("🔄 重新加载", self)
        reload_action.triggered.connect(lambda: self._on_reload_tab(index))
        menu.addAction(reload_action)

        # 添加分隔线
        menu.addSeparator()

        # 关闭选项，添加图标
        close_action = QAction("❌ 关闭", self)
        close_action.triggered.connect(lambda: self._on_close_tab(index))
        menu.addAction(close_action)

        # 显示菜单
        menu.exec_(global_pos)

    def _on_tab_bar_context_menu(self, pos):
        """处理标签栏的上下文菜单请求
        
        Args:
            pos: 上下文菜单请求的位置
        """
        # 获取tabBar
        tab_bar = self._workspace.tabBar()

        # 获取当前右键点击的标签页索引
        index = tab_bar.tabAt(pos)
        if index == -1:  # 没有点击到标签页
            return

        # 创建上下文菜单，使用主窗口作为父对象，避免被遮挡
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)

        # 重新加载选项，添加图标
        reload_action = QAction("🔄 重新加载", self)
        reload_action.triggered.connect(lambda: self._on_reload_tab(index))
        menu.addAction(reload_action)

        # 添加分隔线
        menu.addSeparator()

        # 关闭选项，添加图标
        close_action = QAction("❌ 关闭", self)
        close_action.triggered.connect(lambda: self._on_close_tab(index))
        menu.addAction(close_action)

        # 直接使用全局鼠标位置显示菜单
        menu.exec_(QCursor.pos())

    def _on_new_tab(self, index):
        """处理新建标签页操作
        
        Args:
            index: 当前标签页索引
        """
        # 获取当前标签页的文本
        tab_text = self._workspace.tabText(index)
        # 检查是否是插件标签页
        if tab_text in self._plugin_factories:
            # 使用插件工厂函数创建一个新的标签页实例
            widget_factory = self._plugin_factories[tab_text]
            new_widget = widget_factory()
            self._workspace.addTab(new_widget, tab_text)

    def _on_reload_tab(self, index):
        """处理重新加载标签页操作
        
        Args:
            index: 当前标签页索引
        """
        # 获取当前标签页的文本
        tab_text = self._workspace.tabText(index)
        # 检查是否是插件标签页
        if tab_text in self._plugin_factories:
            # 获取当前标签页的widget
            current_widget = self._workspace.widget(index)

            # 优先尝试调用reset()方法
            if hasattr(current_widget, 'reset') and callable(
                    current_widget.reset):
                try:
                    current_widget.reset()
                    return  # 重置成功，直接返回
                except Exception as e:
                    # 重置失败，继续创建新实例
                    print(f"Failed to reset widget: {e}")

            # 如果没有reset方法或者重置失败，创建新实例
            widget_factory = self._plugin_factories[tab_text]
            new_widget = widget_factory()

            # 保存当前索引
            current_index = self._workspace.currentIndex()

            # 替换当前标签页
            self._workspace.removeTab(index)
            new_index = self._workspace.insertTab(index, new_widget, tab_text)

            # 如果当前标签页是被选中的，切换到新添加的标签页
            if index == current_index:
                self._workspace.setCurrentIndex(new_index)

    def _on_close_tab(self, index):
        """处理关闭标签页操作
        
        Args:
            index: 当前标签页索引
        """
        # 不允许关闭欢迎页面
        if self._workspace.tabText(index) == "欢迎":
            return
        # 关闭当前标签页
        self._workspace.removeTab(index)

        # 检查是否所有标签页都已关闭，如果是，添加欢迎页面
        if self._workspace.count() == 0:
            self._add_welcome_tab()

        self._update_status_label_by_tab()

    def _close_welcome_tab(self):
        """关闭欢迎标签页"""
        # 查找欢迎标签页的索引
        for i in range(self._workspace.count()):
            if self._workspace.tabText(i) == "欢迎":
                # 移除欢迎标签页
                self._workspace.removeTab(i)
                self._update_status_label_by_tab()
                break

    def _update_tab_title(self, widget, title):
        """更新标签页标题
        
        Args:
            widget: 要更新标题的widget
            title: 新标题
        """
        # 查找包含该widget的标签页
        for i in range(self._workspace.count()):
            if self._workspace.widget(i) == widget:
                self._workspace.setTabText(i, title)
                self._update_status_label_by_tab()
                break

    def set_app_instance(self, app_instance):
        """设置应用实例引用
        
        Args:
            app_instance: FugoApp实例
        """
        self._app_instance = app_instance

    def _on_save_triggered(self):
        """处理保存动作
        
        当用户点击文件菜单的保存选项时调用
        """
        from PySide6.QtWidgets import QFileDialog

        # 获取当前活动的标签页
        current_index = self._workspace.currentIndex()
        if current_index < 0:
            return

        # 获取当前标签页的widget
        current_widget = self._workspace.widget(current_index)

        # 检查当前widget是否有save方法
        if hasattr(current_widget, 'save') and callable(current_widget.save):
            # 获取当前标签页名称
            current_tab_text = self._workspace.tabText(current_index)

            # 打开保存文件对话框，默认后缀为.fg，默认名称为当前标签页名称
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存文件", current_tab_text,
                "FugoTools Files (*.fg);;All Files (*)")

            if file_path:
                # 确保文件后缀为.fg
                if not file_path.endswith('.fg'):
                    file_path += '.fg'

                # 调用当前widget的save方法
                current_widget.save(file_path)

    def _on_open_triggered(self):
        """处理打开动作
        
        当用户点击文件菜单的打开选项时调用
        """
        from PySide6.QtWidgets import QFileDialog

        # 获取当前活动的标签页
        current_index = self._workspace.currentIndex()
        if current_index < 0:
            return

        # 获取当前标签页的widget
        current_widget = self._workspace.widget(current_index)

        # 检查当前widget是否有open方法
        if hasattr(current_widget, 'open') and callable(current_widget.open):
            # 打开文件对话框，只允许选择.fg文件
            file_path, _ = QFileDialog.getOpenFileName(
                self, "打开文件", "", "FugoTools Files (*.fg);;All Files (*)")

            if file_path:
                # 调用当前widget的open方法
                current_widget.open(file_path)

    def _on_about_triggered(self):
        """显示关于对话框"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def _on_file_new_triggered(self):
        """处理文件菜单的新建动作
        
        当用户点击文件菜单的新建选项时调用，创建当前标签页的新实例
        """
        # 获取当前活动的标签页
        current_index = self._workspace.currentIndex()
        if current_index < 0:
            return

        # 获取当前标签页的文本
        current_tab_text = self._workspace.tabText(current_index)

        # 检查是否是欢迎页面
        if current_tab_text == "欢迎":
            return

        # 检查当前标签页是否是插件标签页
        if current_tab_text in self._plugin_factories:
            # 使用插件工厂函数创建一个新的标签页实例
            widget_factory = self._plugin_factories[current_tab_text]
            new_widget = widget_factory()
            # 添加新标签页
            self._workspace.addTab(new_widget, current_tab_text)
            # 切换到新添加的标签页
            self._workspace.setCurrentIndex(self._workspace.count() - 1)
            self._update_status_label_by_tab()

    def dragEnterEvent(self, event):
        """全局拖入事件处理 - 转发到当前活动标签页"""
        current_widget = self._workspace.currentWidget()
        if current_widget and hasattr(current_widget, 'dragEnterEvent'):
            # 检查当前标签页是否支持文件导入
            if hasattr(current_widget, 'file_path') or hasattr(current_widget, 'set_file'):
                current_widget.dragEnterEvent(event)
                return
        event.ignore()

    def dropEvent(self, event):
        """全局放下事件处理 - 转发到当前活动标签页"""
        current_widget = self._workspace.currentWidget()
        if current_widget and hasattr(current_widget, 'dropEvent'):
            if hasattr(current_widget, 'file_path') or hasattr(current_widget, 'set_file'):
                current_widget.dropEvent(event)
                return
        event.ignore()
