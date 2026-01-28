"""型钢截面标注计算引擎"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math


class DiagramAnnotator:
    """型钢截面标注计算引擎"""
    
    def __init__(self):
        """初始化标注引擎"""
        # 标注样式配置
        self._config = {
            "font_size": 12,
            "text_color": "#000000",
            "line_color": "#666666",
            "arrow_size": 6,
            "text_offset": 0.05,
            "dimension_line_offset": 0.2,
            "precision": 1  # 小数位数
        }
        
    def create_section_figure(self, shape_data):
        """创建型钢截面的Plotly图形
        
        Args:
            shape_data: 型钢数据字典
            
        Returns:
            plotly.graph_objects.Figure: 型钢截面图形
        """
        shape_type = shape_data.get("类型", "")
        
        if shape_type == "工字钢" or shape_type == "H型钢":
            return self._create_i_figure(shape_data)
        elif shape_type == "槽钢":
            return self._create_channel_figure(shape_data)
        elif shape_type == "角钢":
            return self._create_angle_figure(shape_data)
        elif shape_type == "圆钢":
            return self._create_circle_figure(shape_data)
        elif shape_type == "方钢":
            return self._create_square_figure(shape_data)
        else:
            return self._create_rectangle_figure(shape_data)
            
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
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制高度标注
        self._draw_vertical_dimension(painter, center_x - b * scale / 2 - 20, 
                                    center_y - h * scale / 2, 
                                    center_y + h * scale / 2, 
                                    f"H={h:.{self._config['precision']}f}")
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(painter, center_x - b * scale / 2, 
                                      center_y + h * scale / 2 + 20, 
                                      center_x + b * scale / 2, 
                                      f"B={b:.{self._config['precision']}f}")
        
        # 绘制腹板厚度标注
        self._draw_horizontal_dimension(painter, center_x - t1 * scale / 2, 
                                      center_y - 20, 
                                      center_x + t1 * scale / 2, 
                                      f"t₁={t1:.{self._config['precision']}f}")
        
        # 绘制翼缘厚度标注
        self._draw_vertical_dimension(painter, center_x + b * scale / 2 + 20, 
                                    center_y + h * scale / 2 - t2 * scale, 
                                    center_y + h * scale / 2, 
                                    f"t₂={t2:.{self._config['precision']}f}")
            
    def _draw_channel_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制槽钢尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        t1 = shape_data.get("腹板厚度t1", 5)
        t2 = shape_data.get("翼缘厚度t2", 8)
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制高度标注
        self._draw_vertical_dimension(painter, center_x - 20, 
                                    center_y - h * scale / 2, 
                                    center_y + h * scale / 2, 
                                    f"H={h:.{self._config['precision']}f}")
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(painter, center_x - t1 * scale / 2, 
                                      center_y + h * scale / 2 + 20, 
                                      center_x + (b - t1) * scale / 2, 
                                      f"B={b:.{self._config['precision']}f}")
        
        # 绘制腹板厚度标注
        self._draw_horizontal_dimension(painter, center_x - t1 * scale / 2, 
                                      center_y - 20, 
                                      center_x + t1 * scale / 2, 
                                      f"t₁={t1:.{self._config['precision']}f}")
        
        # 绘制翼缘厚度标注
        self._draw_vertical_dimension(painter, center_x + (b - t1) * scale / 2 + 20, 
                                    center_y + h * scale / 2 - t2 * scale, 
                                    center_y + h * scale / 2, 
                                    f"t₂={t2:.{self._config['precision']}f}")
            
    def _draw_angle_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制角钢尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 100)
        t = shape_data.get("厚度t", 10)
        
        # 计算缩放比例
        max_size = max(h, b)
        scale = min(draw_rect.width() / max_size, draw_rect.height() / max_size) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制高度标注
        self._draw_vertical_dimension(painter, center_x - b * scale / 2 - 20, 
                                    center_y - h * scale / 2, 
                                    center_y + h * scale / 2 - t * scale, 
                                    f"H={h:.{self._config['precision']}f}")
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(painter, center_x - b * scale / 2, 
                                      center_y + h * scale / 2 + 20, 
                                      center_x + b * scale / 2 - t * scale, 
                                      f"B={b:.{self._config['precision']}f}")
        
        # 绘制厚度标注
        self._draw_diagonal_dimension(painter, center_x - b * scale / 2 + t * scale, 
                                    center_y + h * scale / 2 - t * scale, 
                                    center_x - b * scale / 2 + 2 * t * scale, 
                                    center_y + h * scale / 2 - 2 * t * scale, 
                                    f"t={t:.{self._config['precision']}f}")
            
    def _draw_circle_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制圆钢尺寸标注"""
        d = shape_data.get("直径D", 50)
        
        # 计算缩放比例
        scale = min(draw_rect.width() / d, draw_rect.height() / d) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制直径标注
        self._draw_horizontal_dimension(painter, center_x - d * scale / 2, 
                                      center_y + d * scale / 2 + 20, 
                                      center_x + d * scale / 2, 
                                      f"D={d:.{self._config['precision']}f}")
            
    def _draw_square_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制方钢尺寸标注"""
        a = shape_data.get("边长A", 50)
        
        # 计算缩放比例
        scale = min(draw_rect.width() / a, draw_rect.height() / a) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制边长标注
        self._draw_horizontal_dimension(painter, center_x - a * scale / 2, 
                                      center_y + a * scale / 2 + 20, 
                                      center_x + a * scale / 2, 
                                      f"A={a:.{self._config['precision']}f}")
            
    def _draw_rectangle_dimensions(self, painter, shape_data, draw_rect, scale_factor):
        """绘制矩形尺寸标注"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        
        # 计算缩放比例
        scale = min(draw_rect.width() / b, draw_rect.height() / h) * 0.8
        
        # 计算中心点
        center_x = draw_rect.center().x()
        center_y = draw_rect.center().y()
        
        # 绘制高度标注
        self._draw_vertical_dimension(painter, center_x - b * scale / 2 - 20, 
                                    center_y - h * scale / 2, 
                                    center_y + h * scale / 2, 
                                    f"H={h:.{self._config['precision']}f}")
        
        # 绘制宽度标注
        self._draw_horizontal_dimension(painter, center_x - b * scale / 2, 
                                      center_y + h * scale / 2 + 20, 
                                      center_x + b * scale / 2, 
                                      f"B={b:.{self._config['precision']}f}")
            
    def _draw_vertical_dimension(self, painter, x, y1, y2, text):
        """绘制垂直尺寸标注"""
        from PySide6.QtGui import QPen, QColor, QFont
        from PySide6.QtCore import Qt
        
        # 绘制尺寸线
        pen = QPen(QColor(102, 102, 102), 1)
        painter.setPen(pen)
        painter.drawLine(x, y1, x, y2)
        
        # 绘制箭头
        painter.drawLine(x, y1, x - 5, y1 + 10)
        painter.drawLine(x, y1, x + 5, y1 + 10)
        painter.drawLine(x, y2, x - 5, y2 - 10)
        painter.drawLine(x, y2, x + 5, y2 - 10)
        
        # 绘制标注文字
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.drawText(x - 30, (y1 + y2) / 2, text)
            
    def _draw_horizontal_dimension(self, painter, x1, y, x2, text):
        """绘制水平尺寸标注"""
        from PySide6.QtGui import QPen, QColor, QFont
        from PySide6.QtCore import Qt
        
        # 绘制尺寸线
        pen = QPen(QColor(102, 102, 102), 1)
        painter.setPen(pen)
        painter.drawLine(x1, y, x2, y)
        
        # 绘制箭头
        painter.drawLine(x1, y, x1 + 10, y - 5)
        painter.drawLine(x1, y, x1 + 10, y + 5)
        painter.drawLine(x2, y, x2 - 10, y - 5)
        painter.drawLine(x2, y, x2 - 10, y + 5)
        
        # 绘制标注文字
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.drawText((x1 + x2) / 2 - 20, y - 10, text)
            
    def _draw_diagonal_dimension(self, painter, x1, y1, x2, y2, text):
        """绘制对角线尺寸标注"""
        from PySide6.QtGui import QPen, QColor, QFont
        from PySide6.QtCore import Qt
        
        # 绘制尺寸线
        pen = QPen(QColor(102, 102, 102), 1)
        painter.setPen(pen)
        painter.drawLine(x1, y1, x2, y2)
        
        # 绘制箭头
        painter.drawLine(x1, y1, x1 + 5, y1 + 5)
        painter.drawLine(x1, y1, x1 - 5, y1 - 5)
        painter.drawLine(x2, y2, x2 + 5, y2 + 5)
        painter.drawLine(x2, y2, x2 - 5, y2 - 5)
        
        # 绘制标注文字
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.drawText((x1 + x2) / 2, (y1 + y2) / 2 - 10, text)
            
    def _create_i_figure(self, shape_data):
        """创建工字钢/H型钢图形"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        t1 = shape_data.get("腹板厚度t1", 5)
        t2 = shape_data.get("翼缘厚度t2", 8)
        
        # 创建图形
        fig = go.Figure()
        
        # 计算中心点
        center_x = 0
        center_y = 0
        
        # 绘制上翼缘
        fig.add_shape(
            type="rect",
            x0=center_x - b/2,
            y0=center_y - h/2,
            x1=center_x + b/2,
            y1=center_y - h/2 + t2,
            fillcolor="rgba(200, 200, 255, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 绘制下翼缘
        fig.add_shape(
            type="rect",
            x0=center_x - b/2,
            y0=center_y + h/2 - t2,
            x1=center_x + b/2,
            y1=center_y + h/2,
            fillcolor="rgba(200, 200, 255, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 绘制腹板
        fig.add_shape(
            type="rect",
            x0=center_x - t1/2,
            y0=center_y - h/2 + t2,
            x1=center_x + t1/2,
            y1=center_y + h/2 - t2,
            fillcolor="rgba(200, 200, 255, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 添加尺寸标注
        # 高度H
        fig.add_shape(
            type="line",
            x0=-b/2 - 10,
            y0=center_y - h/2,
            x1=-b/2 - 10,
            y1=center_y + h/2,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 高度箭头
        fig.add_annotation(
            x=-b/2 - 12,
            y=center_y - h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=10,
        )
        
        fig.add_annotation(
            x=-b/2 - 12,
            y=center_y + h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=-10,
        )
        
        # 高度标注文字
        fig.add_annotation(
            x=-b/2 - 15,
            y=center_y,
            text=f"H={h:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=-90,
        )
        
        # 宽度B
        fig.add_shape(
            type="line",
            x0=center_x - b/2,
            y0=center_y + h/2 + 10,
            x1=center_x + b/2,
            y1=center_y + h/2 + 10,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 宽度箭头
        fig.add_annotation(
            x=center_x - b/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-10,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + b/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=10,
            ay=0,
        )
        
        # 宽度标注文字
        fig.add_annotation(
            x=center_x,
            y=center_y + h/2 + 18,
            text=f"B={b:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 腹板厚度t1
        fig.add_shape(
            type="line",
            x0=center_x - t1/2,
            y0=center_y - 20,
            x1=center_x + t1/2,
            y1=center_y - 20,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 腹板厚度箭头
        fig.add_annotation(
            x=center_x - t1/2,
            y=center_y - 22,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-5,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + t1/2,
            y=center_y - 22,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=5,
            ay=0,
        )
        
        # 腹板厚度标注文字
        fig.add_annotation(
            x=center_x,
            y=center_y - 28,
            text=f"t₁={t1:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 翼缘厚度t2
        fig.add_shape(
            type="line",
            x0=center_x + b/2 + 10,
            y0=center_y + h/2 - t2,
            x1=center_x + b/2 + 10,
            y1=center_y + h/2,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 翼缘厚度箭头
        fig.add_annotation(
            x=center_x + b/2 + 12,
            y=center_y + h/2 - t2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=-10,
        )
        
        fig.add_annotation(
            x=center_x + b/2 + 12,
            y=center_y + h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=10,
        )
        
        # 翼缘厚度标注文字
        fig.add_annotation(
            x=center_x + b/2 + 15,
            y=center_y + h/2 - t2/2,
            text=f"t₂={t2:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=90,
        )
        
        # 设置布局
        fig.update_layout(
            title="工字钢/H型钢截面",
            xaxis=dict(
                range=[-b/2 - 30, b/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-h/2 - 30, h/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1,
            ),
            width=600,
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig
        
    def _create_channel_figure(self, shape_data):
        """创建槽钢图形"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        t1 = shape_data.get("腹板厚度t1", 5)
        t2 = shape_data.get("翼缘厚度t2", 8)
        
        # 创建图形
        fig = go.Figure()
        
        # 计算中心点
        center_x = 0
        center_y = 0
        
        # 绘制腹板
        fig.add_shape(
            type="rect",
            x0=center_x - t1/2,
            y0=center_y - h/2,
            x1=center_x + t1/2,
            y1=center_y + h/2,
            fillcolor="rgba(255, 200, 200, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 绘制上翼缘
        fig.add_shape(
            type="rect",
            x0=center_x + t1/2,
            y0=center_y - h/2,
            x1=center_x + b - t1/2,
            y1=center_y - h/2 + t2,
            fillcolor="rgba(255, 200, 200, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 绘制下翼缘
        fig.add_shape(
            type="rect",
            x0=center_x + t1/2,
            y0=center_y + h/2 - t2,
            x1=center_x + b - t1/2,
            y1=center_y + h/2,
            fillcolor="rgba(255, 200, 200, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 添加尺寸标注
        # 高度H
        fig.add_shape(
            type="line",
            x0=-10,
            y0=center_y - h/2,
            x1=-10,
            y1=center_y + h/2,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 高度箭头
        fig.add_annotation(
            x=-12,
            y=center_y - h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=10,
        )
        
        fig.add_annotation(
            x=-12,
            y=center_y + h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=-10,
        )
        
        # 高度标注文字
        fig.add_annotation(
            x=-15,
            y=center_y,
            text=f"H={h:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=-90,
        )
        
        # 宽度B
        fig.add_shape(
            type="line",
            x0=center_x - t1/2,
            y0=center_y + h/2 + 10,
            x1=center_x + b - t1/2,
            y1=center_y + h/2 + 10,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 宽度箭头
        fig.add_annotation(
            x=center_x - t1/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-10,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + b - t1/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=10,
            ay=0,
        )
        
        # 宽度标注文字
        fig.add_annotation(
            x=center_x + (b - t1)/2,
            y=center_y + h/2 + 18,
            text=f"B={b:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 腹板厚度t1
        fig.add_shape(
            type="line",
            x0=center_x - t1/2,
            y0=center_y - 20,
            x1=center_x + t1/2,
            y1=center_y - 20,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 腹板厚度箭头
        fig.add_annotation(
            x=center_x - t1/2,
            y=center_y - 22,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-5,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + t1/2,
            y=center_y - 22,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=5,
            ay=0,
        )
        
        # 腹板厚度标注文字
        fig.add_annotation(
            x=center_x,
            y=center_y - 28,
            text=f"t₁={t1:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 翼缘厚度t2
        fig.add_shape(
            type="line",
            x0=center_x + b - t1/2 + 10,
            y0=center_y + h/2 - t2,
            x1=center_x + b - t1/2 + 10,
            y1=center_y + h/2,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 翼缘厚度箭头
        fig.add_annotation(
            x=center_x + b - t1/2 + 12,
            y=center_y + h/2 - t2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=-10,
        )
        
        fig.add_annotation(
            x=center_x + b - t1/2 + 12,
            y=center_y + h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=10,
        )
        
        # 翼缘厚度标注文字
        fig.add_annotation(
            x=center_x + b - t1/2 + 15,
            y=center_y + h/2 - t2/2,
            text=f"t₂={t2:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=90,
        )
        
        # 设置布局
        fig.update_layout(
            title="槽钢截面",
            xaxis=dict(
                range=[-20, b + 20],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-h/2 - 30, h/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1,
            ),
            width=600,
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig
        
    def _create_angle_figure(self, shape_data):
        """创建角钢图形"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 100)
        t = shape_data.get("厚度t", 10)
        
        # 创建图形
        fig = go.Figure()
        
        # 计算中心点
        center_x = 0
        center_y = 0
        
        # 绘制角钢
        fig.add_shape(
            type="path",
            path=f"M {-b/2}, {-h/2} L {b/2}, {-h/2} L {b/2}, {-h/2 + t} L {-b/2 + t}, {-h/2 + t} L {-b/2 + t}, {h/2 - t} L {-b/2}, {h/2 - t} Z",
            fillcolor="rgba(200, 255, 200, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 添加尺寸标注
        # 高度H
        fig.add_shape(
            type="line",
            x0=-b/2 - 10,
            y0=center_y - h/2,
            x1=-b/2 - 10,
            y1=center_y + h/2 - t,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 高度箭头
        fig.add_annotation(
            x=-b/2 - 12,
            y=center_y - h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=10,
        )
        
        fig.add_annotation(
            x=-b/2 - 12,
            y=center_y + h/2 - t,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=-10,
        )
        
        # 高度标注文字
        fig.add_annotation(
            x=-b/2 - 15,
            y=center_y - t/2,
            text=f"H={h - t:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=-90,
        )
        
        # 宽度B
        fig.add_shape(
            type="line",
            x0=center_x - b/2,
            y0=center_y + h/2 + 10,
            x1=center_x + b/2 - t,
            y1=center_y + h/2 + 10,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 宽度箭头
        fig.add_annotation(
            x=center_x - b/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-10,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + b/2 - t,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=10,
            ay=0,
        )
        
        # 宽度标注文字
        fig.add_annotation(
            x=center_x + (b/2 - t/2),
            y=center_y + h/2 + 18,
            text=f"B={b - t:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 厚度t
        fig.add_shape(
            type="line",
            x0=center_x - b/2 + t,
            y0=center_y + h/2 - t,
            x1=center_x - b/2 + 2*t,
            y1=center_y + h/2 - 2*t,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 厚度箭头
        fig.add_annotation(
            x=center_x - b/2 + t,
            y=center_y + h/2 - t,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-5,
            ay=5,
        )
        
        fig.add_annotation(
            x=center_x - b/2 + 2*t,
            y=center_y + h/2 - 2*t,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=5,
            ay=-5,
        )
        
        # 厚度标注文字
        fig.add_annotation(
            x=center_x - b/2 + 1.5*t,
            y=center_y + h/2 - 1.5*t,
            text=f"t={t:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=45,
        )
        
        # 设置布局
        fig.update_layout(
            title="角钢截面",
            xaxis=dict(
                range=[-b/2 - 30, b/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-h/2 - 30, h/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1,
            ),
            width=600,
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig
        
    def _create_circle_figure(self, shape_data):
        """创建圆钢图形"""
        d = shape_data.get("直径D", 50)
        
        # 创建图形
        fig = go.Figure()
        
        # 计算中心点
        center_x = 0
        center_y = 0
        
        # 绘制圆形
        fig.add_shape(
            type="circle",
            x0=center_x - d/2,
            y0=center_y - d/2,
            x1=center_x + d/2,
            y1=center_y + d/2,
            fillcolor="rgba(255, 255, 200, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 添加直径标注
        fig.add_shape(
            type="line",
            x0=center_x - d/2,
            y0=center_y + d/2 + 10,
            x1=center_x + d/2,
            y1=center_y + d/2 + 10,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 直径箭头
        fig.add_annotation(
            x=center_x - d/2,
            y=center_y + d/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-10,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + d/2,
            y=center_y + d/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=10,
            ay=0,
        )
        
        # 直径标注文字
        fig.add_annotation(
            x=center_x,
            y=center_y + d/2 + 18,
            text=f"D={d:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 设置布局
        fig.update_layout(
            title="圆钢截面",
            xaxis=dict(
                range=[-d/2 - 30, d/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-d/2 - 30, d/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1,
            ),
            width=500,
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig
        
    def _create_square_figure(self, shape_data):
        """创建方钢图形"""
        a = shape_data.get("边长A", 50)
        
        # 创建图形
        fig = go.Figure()
        
        # 计算中心点
        center_x = 0
        center_y = 0
        
        # 绘制方形
        fig.add_shape(
            type="rect",
            x0=center_x - a/2,
            y0=center_y - a/2,
            x1=center_x + a/2,
            y1=center_y + a/2,
            fillcolor="rgba(200, 255, 255, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 添加边长标注
        fig.add_shape(
            type="line",
            x0=center_x - a/2,
            y0=center_y + a/2 + 10,
            x1=center_x + a/2,
            y1=center_y + a/2 + 10,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 边长箭头
        fig.add_annotation(
            x=center_x - a/2,
            y=center_y + a/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-10,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + a/2,
            y=center_y + a/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=10,
            ay=0,
        )
        
        # 边长标注文字
        fig.add_annotation(
            x=center_x,
            y=center_y + a/2 + 18,
            text=f"A={a:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 设置布局
        fig.update_layout(
            title="方钢截面",
            xaxis=dict(
                range=[-a/2 - 30, a/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-a/2 - 30, a/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1,
            ),
            width=500,
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig
        
    def _create_rectangle_figure(self, shape_data):
        """创建矩形图形"""
        h = shape_data.get("高度H", 100)
        b = shape_data.get("宽度B", 50)
        
        # 创建图形
        fig = go.Figure()
        
        # 计算中心点
        center_x = 0
        center_y = 0
        
        # 绘制矩形
        fig.add_shape(
            type="rect",
            x0=center_x - b/2,
            y0=center_y - h/2,
            x1=center_x + b/2,
            y1=center_y + h/2,
            fillcolor="rgba(240, 240, 240, 0.7)",
            line=dict(color="#000000", width=2),
        )
        
        # 添加尺寸标注
        # 高度H
        fig.add_shape(
            type="line",
            x0=-b/2 - 10,
            y0=center_y - h/2,
            x1=-b/2 - 10,
            y1=center_y + h/2,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 高度箭头
        fig.add_annotation(
            x=-b/2 - 12,
            y=center_y - h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=10,
        )
        
        fig.add_annotation(
            x=-b/2 - 12,
            y=center_y + h/2,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=0,
            ay=-10,
        )
        
        # 高度标注文字
        fig.add_annotation(
            x=-b/2 - 15,
            y=center_y,
            text=f"H={h:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
            textangle=-90,
        )
        
        # 宽度B
        fig.add_shape(
            type="line",
            x0=center_x - b/2,
            y0=center_y + h/2 + 10,
            x1=center_x + b/2,
            y1=center_y + h/2 + 10,
            line=dict(color=self._config["line_color"], width=1),
        )
        
        # 宽度箭头
        fig.add_annotation(
            x=center_x - b/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=-10,
            ay=0,
        )
        
        fig.add_annotation(
            x=center_x + b/2,
            y=center_y + h/2 + 12,
            text="",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=self._config["line_color"],
            ax=10,
            ay=0,
        )
        
        # 宽度标注文字
        fig.add_annotation(
            x=center_x,
            y=center_y + h/2 + 18,
            text=f"B={b:.{self._config['precision']}f}",
            showarrow=False,
            font=dict(size=self._config["font_size"], color=self._config["text_color"]),
        )
        
        # 设置布局
        fig.update_layout(
            title="矩形截面",
            xaxis=dict(
                range=[-b/2 - 30, b/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-h/2 - 30, h/2 + 30],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor="x",
                scaleratio=1,
            ),
            width=600,
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        return fig