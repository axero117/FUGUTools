"""型钢截面标注计算引擎"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QFont, QPainterPath, QColor
import math


class DiagramAnnotator:
    """型钢截面标注计算引擎"""
    
    def __init__(self):
        """初始化标注引擎"""
        # 标注样式配置
        self._config = {
            "font_size": 10,
            "text_color": QColor(0, 0, 0),
            "line_color": QColor(100, 100, 100),
            "arrow_size": 6,
            "text_offset": 5,
            "dimension_line_offset": 20,
            "precision": 1  # 小数位数
        }
        
    def draw_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制尺寸标注
        
        Args:
            painter: QPainter对象
            shape_data: 型钢数据字典
            draw_rect: 绘图区域
            scale_factor: 缩放因子
        """
        shape_type = shape_data.get("类型", "")
        
        if shape_type == "工字钢" or shape_type == "H型钢":
            self._draw_i_dimensions(painter, shape_data, draw_rect, scale_factor)
        elif shape_type == "槽钢":
            self._draw_channel_dimensions(painter, shape_data, draw_rect, scale_factor)
        elif shape_type == "角钢":
            self._draw_angle_dimensions(painter, shape_data, draw_rect, scale_factor)
        elif shape_type == "圆钢":
            self._draw_circle_dimensions(painter, shape_data, draw_rect, scale_factor)
        elif shape_type == "方钢":
            self._draw_square_dimensions(painter, shape_data, draw_rect, scale_factor)
        else:
            self._draw_rectangle_dimensions(painter, shape_data, draw_rect, scale_factor)
            
    def _draw_i_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制工字钢/H型钢尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        t1 = shape_data.get("腹板厚度t1", 5)
        t2 = shape_data.get("翼缘厚度t2", 8)
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 绘制高度标注
        self._draw_vertical_dimension(
            painter, 
            center_x - b * scale / 2 - 40,  # 标注线位置
            center_y - h * scale / 2,       # 起点
            center_y + h * scale / 2,       # 终点
            h,                                # 尺寸值
            "H"
        )
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(
            painter,
            center_x - b * scale / 2,       # 起点
            center_x + b * scale / 2,       # 终点
            center_y + h * scale / 2 + 40,  # 标注线位置
            b,                                # 尺寸值
            "B"
        )
        
        # 绘制腹板厚度标注
        self._draw_horizontal_dimension(
            painter,
            center_x - t1 * scale / 2,
            center_x + t1 * scale / 2,
            center_y - 30,
            t1,
            "t₁"
        )
        
        # 绘制翼缘厚度标注
        self._draw_vertical_dimension(
            painter,
            center_x + b * scale / 2 + 30,
            center_y + h * scale / 2 - t2 * scale,
            center_y + h * scale / 2,
            t2,
            "t₂"
        )
        
    def _draw_channel_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制槽钢尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        t1 = shape_data.get("腹板厚度t1", 5)
        t2 = shape_data.get("翼缘厚度t2", 8)
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 绘制高度标注
        self._draw_vertical_dimension(
            painter,
            center_x - t1 * scale / 2 - 40,
            center_y - h * scale / 2,
            center_y + h * scale / 2,
            h,
            "H"
        )
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(
            painter,
            center_x - t1 * scale / 2,
            center_x + b * scale / 2,
            center_y + h * scale / 2 + 40,
            b,
            "B"
        )
        
        # 绘制腹板厚度标注
        self._draw_horizontal_dimension(
            painter,
            center_x - t1 * scale / 2,
            center_x + t1 * scale / 2,
            center_y - 30,
            t1,
            "t₁"
        )
        
        # 绘制翼缘厚度标注
        self._draw_vertical_dimension(
            painter,
            center_x + b * scale / 2 + 30,
            center_y + h * scale / 2 - t2 * scale,
            center_y + h * scale / 2,
            t2,
            "t₂"
        )
        
    def _draw_angle_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制角钢尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 100)
        t = shape_data.get("厚度t", 10)
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 绘制高度标注
        self._draw_vertical_dimension(
            painter,
            center_x - b * scale / 2 - 40,
            center_y - h * scale / 2,
            center_y + h * scale / 2 - t * scale,
            h - t,
            "H"
        )
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(
            painter,
            center_x - b * scale / 2,
            center_x + b * scale / 2 - t * scale,
            center_y + h * scale / 2 + 40,
            b - t,
            "B"
        )
        
        # 绘制厚度标注
        self._draw_diagonal_dimension(
            painter,
            center_x - b * scale / 2 + t * scale,
            center_y + h * scale / 2 - t * scale,
            center_x - b * scale / 2 + 2 * t * scale,
            center_y + h * scale / 2 - 2 * t * scale,
            t,
            "t"
        )
        
    def _draw_circle_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制圆钢尺寸标注"""
        d = shape_data.get("直径D", 50)
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制直径标注
        self._draw_horizontal_dimension(
            painter,
            center_x - d * scale_factor / 2,
            center_x + d * scale_factor / 2,
            center_y + d * scale_factor / 2 + 40,
            d,
            "D"
        )
        
    def _draw_square_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制方钢尺寸标注"""
        a = shape_data.get("边长A", 50)
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制边长标注
        self._draw_horizontal_dimension(
            painter,
            center_x - a * scale_factor / 2,
            center_x + a * scale_factor / 2,
            center_y + a * scale_factor / 2 + 40,
            a,
            "A"
        )
        
    def _draw_rectangle_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制矩形尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制高度标注
        self._draw_vertical_dimension(
            painter,
            center_x - b * scale_factor / 2 - 40,
            center_y - h * scale_factor / 2,
            center_y + h * scale_factor / 2,
            h,
            "H"
        )
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(
            painter,
            center_x - b * scale_factor / 2,
            center_x + b * scale_factor / 2,
            center_y + h * scale_factor / 2 + 40,
            b,
            "B"
        )
        
    def _draw_horizontal_dimension(self, painter, x1, x2, y_pos, value, label):
        """绘制水平尺寸标注
        
        Args:
            painter: QPainter对象
            x1: 起点X坐标
            x2: 终点X坐标
            y_pos: 标注线Y坐标
            value: 尺寸值
            label: 标签文字
        """
        # 设置画笔
        painter.setPen(QPen(self._config["line_color"], 1))
        
        # 绘制尺寸线
        painter.drawLine(x1, y_pos, x2, y_pos)
        
        # 绘制箭头
        self._draw_arrow(painter, x1, y_pos, 180)  # 左箭头
        self._draw_arrow(painter, x2, y_pos, 0)    # 右箭头
        
        # 绘制延伸线
        painter.drawLine(x1, y_pos - 10, x1, y_pos + 10)
        painter.drawLine(x2, y_pos - 10, x2, y_pos + 10)
        
        # 绘制尺寸文字
        text = f"{label}={value:.{self._config['precision']}f}"
        font = QFont("Arial", self._config["font_size"])
        painter.setFont(font)
        
        text_rect = painter.boundingRect(0, 0, 0, 0, Qt.AlignCenter, text)
        text_x = (x1 + x2) / 2 - text_rect.width() / 2
        text_y = y_pos - self._config["text_offset"]
        
        painter.setPen(QPen(self._config["text_color"]))
        painter.drawText(text_x, text_y, text)
        
    def _draw_vertical_dimension(self, painter, x_pos, y1, y2, value, label):
        """绘制垂直尺寸标注
        
        Args:
            painter: QPainter对象
            x_pos: 标注线X坐标
            y1: 起点Y坐标
            y2: 终点Y坐标
            value: 尺寸值
            label: 标签文字
        """
        # 设置画笔
        painter.setPen(QPen(self._config["line_color"], 1))
        
        # 绘制尺寸线
        painter.drawLine(x_pos, y1, x_pos, y2)
        
        # 绘制箭头
        self._draw_arrow(painter, x_pos, y1, 90)   # 上箭头
        self._draw_arrow(painter, x_pos, y2, 270)  # 下箭头
        
        # 绘制延伸线
        painter.drawLine(x_pos - 10, y1, x_pos + 10, y1)
        painter.drawLine(x_pos - 10, y2, x_pos + 10, y2)
        
        # 绘制尺寸文字
        text = f"{label}={value:.{self._config['precision']}f}"
        font = QFont("Arial", self._config["font_size"])
        painter.setFont(font)
        
        text_rect = painter.boundingRect(0, 0, 0, 0, Qt.AlignCenter, text)
        text_x = x_pos + self._config["text_offset"]
        text_y = (y1 + y2) / 2 + text_rect.height() / 2
        
        painter.setPen(QPen(self._config["text_color"]))
        painter.drawText(text_x, text_y, text)
        
    def _draw_diagonal_dimension(self, painter, x1, y1, x2, y2, value, label):
        """绘制斜向尺寸标注"""
        # 设置画笔
        painter.setPen(QPen(self._config["line_color"], 1))
        
        # 绘制尺寸线
        painter.drawLine(x1, y1, x2, y2)
        
        # 绘制箭头
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        self._draw_arrow(painter, x1, y1, angle + 180)
        self._draw_arrow(painter, x2, y2, angle)
        
        # 绘制尺寸文字
        text = f"{label}={value:.{self._config['precision']}f}"
        font = QFont("Arial", self._config["font_size"])
        painter.setFont(font)
        
        text_rect = painter.boundingRect(0, 0, 0, 0, Qt.AlignCenter, text)
        text_x = (x1 + x2) / 2 - text_rect.width() / 2
        text_y = (y1 + y2) / 2 + text_rect.height() / 2
        
        painter.setPen(QPen(self._config["text_color"]))
        painter.drawText(text_x, text_y, text)
        
    def _draw_arrow(self, painter, x, y, angle):
        """绘制箭头
        
        Args:
            painter: QPainter对象
            x: 箭头位置X坐标
            y: 箭头位置Y坐标
            angle: 箭头方向角度（度）
        """
        arrow_size = self._config["arrow_size"]
        
        # 计算箭头方向
        angle_rad = math.radians(angle)
        dx1 = arrow_size * math.cos(angle_rad - math.pi / 6)
        dy1 = arrow_size * math.sin(angle_rad - math.pi / 6)
        dx2 = arrow_size * math.cos(angle_rad + math.pi / 6)
        dy2 = arrow_size * math.sin(angle_rad + math.pi / 6)
        
        # 绘制箭头
        painter.drawLine(x, y, x - dx1, y - dy1)
        painter.drawLine(x, y, x - dx2, y - dy2)