"""型钢截面形状绘图组件"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath

from plugins.Steel_Shape_Table.ui.diagram_annotator import DiagramAnnotator


class SectionDiagram(QWidget):
    """型钢截面形状绘图组件"""
    
    def __init__(self, parent=None):
        """初始化绘图组件"""
        super().__init__(parent)
        self._shape_data = None
        self._scale_factor = 1.0
        self._offset = QPointF(0, 0)
        self._margin = 50  # 边距
        
        # 创建标注引擎
        self._annotator = DiagramAnnotator()
        
        # 设置最小尺寸
        self.setMinimumSize(400, 300)
        
        # 启用鼠标事件用于缩放和平移
        self.setMouseTracking(True)
        self._last_mouse_pos = None
        
    def set_shape_data(self, shape_data):
        """设置型钢数据
        
        Args:
            shape_data: 型钢数据字典，包含截面参数
        """
        self._shape_data = shape_data
        self.update()  # 重绘
        
    def set_scale_factor(self, scale):
        """设置缩放因子
        
        Args:
            scale: 缩放因子
        """
        self._scale_factor = scale
        self.update()  # 重绘
        
    def reset_view(self):
        """重置视图"""
        self._scale_factor = 1.0
        self._offset = QPointF(0, 0)
        self.update()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 填充背景
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        
        # 如果没有数据，显示提示信息
        if not self._shape_data:
            self._draw_no_data(painter)
            return
            
        # 保存绘图状态
        painter.save()
        
        # 应用缩放和平移
        painter.translate(self._offset)
        painter.scale(self._scale_factor, self._scale_factor)
        
        # 获取绘图区域
        draw_rect = QRectF(
            self._margin / self._scale_factor,
            self._margin / self._scale_factor,
            (self.width() - 2 * self._margin) / self._scale_factor,
            (self.height() - 2 * self._margin) / self._scale_factor
        )
        
        # 绘制截面形状
        self._draw_section_shape(painter, draw_rect)
        
        # 绘制尺寸标注
        self._draw_dimensions(painter, draw_rect)
        
        # 恢复绘图状态
        painter.restore()
        
    def _draw_no_data(self, painter):
        """绘制无数据提示"""
        painter.setPen(QPen(QColor(128, 128, 128)))
        font = QFont("Arial", 12)
        painter.setFont(font)
        
        text = "请选择型钢型号"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, text)
        painter.drawText(text_rect, Qt.AlignCenter, text)
        
    def _draw_section_shape(self, painter, draw_rect):
        """绘制截面形状
        
        Args:
            painter: QPainter对象
            draw_rect: 绘图区域
        """
        shape_type = self._shape_data.get("类型", "")
        
        if shape_type == "工字钢" or shape_type == "H型钢":
            self._draw_i_shape(painter, draw_rect)
        elif shape_type == "槽钢":
            self._draw_channel_shape(painter, draw_rect)
        elif shape_type == "角钢":
            self._draw_angle_shape(painter, draw_rect)
        elif shape_type == "圆钢":
            self._draw_circle_shape(painter, draw_rect)
        elif shape_type == "方钢":
            self._draw_square_shape(painter, draw_rect)
        else:
            # 默认绘制矩形
            self._draw_rectangle_shape(painter, draw_rect)
            
    def _draw_i_shape(self, painter, draw_rect):
        """绘制工字钢/H型钢截面"""
        h = self._shape_data.get("高度H", 100)
        b = self._shape_data.get("宽度B", 50)
        t1 = self._shape_data.get("腹板厚度t1", 5)
        t2 = self._shape_data.get("翼缘厚度t2", 8)
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制截面
        path = QPainterPath()
        
        # 上翼缘
        path.addRect(center_x - b * scale / 2, center_y - h * scale / 2, b * scale, t2 * scale)
        
        # 下翼缘
        path.addRect(center_x - b * scale / 2, center_y + h * scale / 2 - t2 * scale, b * scale, t2 * scale)
        
        # 腹板
        path.addRect(center_x - t1 * scale / 2, center_y - h * scale / 2 + t2 * scale, t1 * scale, h * scale - 2 * t2 * scale)
        
        # 填充颜色
        painter.fillPath(path, QBrush(QColor(200, 200, 255, 180)))
        
        # 绘制轮廓
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawPath(path)
        
    def _draw_channel_shape(self, painter, draw_rect):
        """绘制槽钢截面"""
        h = self._shape_data.get("高度H", 100)
        b = self._shape_data.get("宽度B", 50)
        t1 = self._shape_data.get("腹板厚度t1", 5)
        t2 = self._shape_data.get("翼缘厚度t2", 8)
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制截面
        path = QPainterPath()
        
        # 腹板
        path.addRect(center_x - t1 * scale / 2, center_y - h * scale / 2, t1 * scale, h * scale)
        
        # 上翼缘
        path.addRect(center_x + t1 * scale / 2, center_y - h * scale / 2, (b - t1) * scale, t2 * scale)
        
        # 下翼缘
        path.addRect(center_x + t1 * scale / 2, center_y + h * scale / 2 - t2 * scale, (b - t1) * scale, t2 * scale)
        
        # 填充颜色
        painter.fillPath(path, QBrush(QColor(255, 200, 200, 180)))
        
        # 绘制轮廓
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawPath(path)
        
    def _draw_angle_shape(self, painter, draw_rect):
        """绘制角钢截面"""
        h = self._shape_data.get("高度H", 100)
        b = self._shape_data.get("宽度B", 100)
        t = self._shape_data.get("厚度t", 10)
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制截面
        path = QPainterPath()
        
        # 外轮廓
        path.moveTo(center_x - b * scale / 2, center_y - h * scale / 2)
        path.lineTo(center_x + b * scale / 2, center_y - h * scale / 2)
        path.lineTo(center_x + b * scale / 2, center_y - h * scale / 2 + t * scale)
        path.lineTo(center_x - b * scale / 2 + t * scale, center_y - h * scale / 2 + t * scale)
        path.lineTo(center_x - b * scale / 2 + t * scale, center_y + h * scale / 2 - t * scale)
        path.lineTo(center_x - b * scale / 2, center_y + h * scale / 2 - t * scale)
        path.lineTo(center_x - b * scale / 2, center_y - h * scale / 2)
        
        # 填充颜色
        painter.fillPath(path, QBrush(QColor(200, 255, 200, 180)))
        
        # 绘制轮廓
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawPath(path)
        
    def _draw_circle_shape(self, painter, draw_rect):
        """绘制圆钢截面"""
        d = self._shape_data.get("直径D", 50)
        
        # 计算缩放比例
        scale = min(draw_rect.width() / d, draw_rect.height() / d) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制圆形
        painter.setBrush(QBrush(QColor(255, 255, 200, 180)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(center_x - d * scale / 2, center_y - d * scale / 2, d * scale, d * scale)
        
    def _draw_square_shape(self, painter, draw_rect):
        """绘制方钢截面"""
        a = self._shape_data.get("边长A", 50)
        
        # 计算缩放比例
        scale = min(draw_rect.width() / a, draw_rect.height() / a) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制方形
        painter.setBrush(QBrush(QColor(200, 255, 255, 180)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(center_x - a * scale / 2, center_y - a * scale / 2, a * scale, a * scale)
        
    def _draw_rectangle_shape(self, painter, draw_rect):
        """绘制矩形截面（默认）"""
        h = self._shape_data.get("高度H", 100)
        b = self._shape_data.get("宽度B", 50)
        
        # 计算缩放比例
        scale = min(draw_rect.width() / b, draw_rect.height() / h) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制矩形
        painter.setBrush(QBrush(QColor(240, 240, 240, 180)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(center_x - b * scale / 2, center_y - h * scale / 2, b * scale, h * scale)
        
    def _draw_dimensions(self, painter, draw_rect):
        """绘制尺寸标注"""
        if self._shape_data and self._annotator:
            self._annotator.draw_dimensions(painter, self._shape_data, draw_rect, self._scale_factor)
        
    def wheelEvent(self, event):
        """鼠标滚轮事件，用于缩放"""
        # 获取滚轮增量
        delta = event.angleDelta().y()
        
        # 计算缩放因子
        if delta > 0:
            scale_factor = 1.1
        else:
            scale_factor = 0.9
            
        # 限制缩放范围
        new_scale = self._scale_factor * scale_factor
        if 0.1 <= new_scale <= 5.0:
            self._scale_factor = new_scale
            self.update()
            
        event.accept()
        
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self._last_mouse_pos = event.pos()
            
    def mouseMoveEvent(self, event):
        """鼠标移动事件，用于平移"""
        if event.buttons() & Qt.LeftButton and self._last_mouse_pos is not None:
            delta = event.pos() - self._last_mouse_pos
            self._offset += delta
            self._last_mouse_pos = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._last_mouse_pos = None