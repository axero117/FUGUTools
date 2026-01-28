"""数据库操作模块"""

from re import I
import sqlite3
import json
import os
from tkinter import W
from typing import List, Optional
from plugins.Steel_Shape_Table.models import SteelSection


class SectionDatabase:
    """型钢截面数据库操作类"""
    
    def __init__(self, db_path: str):
        """初始化数据库连接
        
        Args:
            db_path: 数据库文件路径
        """
        self._db_path = db_path
        self._cache = {}
        self._init_db()

        # 初始化缓存
        self._load_cache()

    def _init_db(self):
        """初始化数据库
        
        只做必要的初始化工作，不创建表结构
        """
        # 确保数据库文件所在目录存在
        db_dir = os.path.dirname(self._db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # 测试数据库连接
        try:
            with sqlite3.connect(self._db_path) as conn:
                # 简单执行一个查询来测试连接
                conn.execute("SELECT 1")
        except sqlite3.Error as e:
            print(f"数据库连接测试失败: {e}")
    
    def _load_cache(self):
        """加载缓存"""
        # 获取所有型钢类型
        shape_types = self.get_shape_types()
        for shape_type in shape_types:
            # 预加载每种类型的前100条数据到缓存
            sections = self.get_sections(shape_type, limit=100)
            self._cache[shape_type] = sections

    def _get_sections_from_h_sections_table(self, category: str, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从h_sections_2017表获取型钢截面数据
        
        Args:
            category: 型钢类别 (HW/HM/HN/HP等)
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM h_sections_2017 WHERE category = ?"
            params = [category]
            
            # 添加关键词搜索
            if keyword:
                query += " AND section_name LIKE ?"
                params.append(f"%{keyword}%")
            
            # 添加限制
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为SteelSection对象
            sections = []
            for row in rows:
                section = SteelSection(
                    shape_type="H型钢截面表（2017）",  # 固定为H型钢截面表（2017）
                    category=row['category'],  # 类别作为category
                    model=row['section_name'],  # section_name作为model
                    height=row['height'],
                    width=row['width'],
                    web_thickness=row['web_thickness'],
                    flange_thickness=row['flange_thickness'],
                    fillet_radius=row['fillet_radius'],  # 使用数据库中的圆角半径
                    area=row['area'],
                    weight=row['weight'],
                    surface_area=row['surface_area'],  # 使用数据库中的表面积
                    Ix=row['Ix'],  # Ix对应数据库中的Ix列
                    Iy=row['Iy'],  # Iy对应数据库中的Iy列
                    ix=row['rx'],  # 惯性半径ix
                    iy=row['ry'],  # 惯性半径iy
                    Wx=row['Wx'],  # Wx对应数据库中的Wx列
                    Wy=row['Wy']   # Wy对应数据库中的Wy列
                )
                sections.append(section)
            
            return sections
            
    def _get_sections_from_h_sections_2024_table(self, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从h_sections_2024表获取型钢截面数据
        
        Args:
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM h_sections_2024"
            params = []
            
            # 添加关键词搜索
            if keyword:
                query += " WHERE section_name LIKE ?"
                params.append(f"%{keyword}%")
            
            # 添加限制
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为SteelSection对象
            sections = []
            for row in rows:
                section = SteelSection(
                    shape_type="H型钢截面表（2024）",  # 统一使用"H型钢截面表（2024）"作为shape_type
                    model=row['section_name'],  # section_name作为model
                    height=row['height'],
                    width=row['width'],
                    web_thickness=row['web_thickness'],
                    flange_thickness=row['flange_thickness'],
                    fillet_radius=row['fillet_radius'],  # 使用数据库中的圆角半径
                    area=row['area'],
                    weight=row['weight'],
                    surface_area=row['surface_area'],  # 使用数据库中的表面积
                    Ix=row['Ix'],  # Ix对应数据库中的Ix列
                    Iy=row['Iy'],  # Iy对应数据库中的Iy列
                    ix=row['rx'],  # 惯性半径ix
                    iy=row['ry'],  # 惯性半径iy
                    Wx=row['Wx'],  # Wx对应数据库中的Wx列
                    Wy=row['Wy']   # Wy对应数据库中的Wy列
                )
                sections.append(section)
            
            return sections
            
    def _get_sections_from_i_sections_2016_table(self, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从i_sections_2016表获取型钢截面数据
        
        Args:
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM i_sections_2016"
            params = []
            
            # 添加关键词搜索
            if keyword:
                query += " WHERE section_name LIKE ?"
                params.append(f"%{keyword}%")
            
            # 添加限制
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为SteelSection对象
            sections = []
            for row in rows:
                section = SteelSection(
                    shape_type="I型钢截面表（2016）",  # 统一使用"I型钢截面表（2016）"作为shape_type
                    model=row['section_name'],  # section_name作为model
                    height=row['height'],
                    width=row['width'],
                    web_thickness=row['web_thickness'],
                    flange_thickness=row['flange_thickness'],
                    inner_fillet_radius=row['inner_fillet_radius'],  # 内圆角半径
                    round_radius=row['round_radius'],  # 使用数据库中的圆角半径
                    area=row['area'],
                    weight=row['weight'],
                    surface_area=row['surface_area'],  # 使用数据库中的表面积
                    Ix=row['Ix'],  # Ix对应数据库中的Ix列
                    Iy=row['Iy'],  # Iy对应数据库中的Iy列
                    ix=row['rx'],  # 惯性半径ix
                    iy=row['ry'],  # 惯性半径iy
                    Wx=row['Wx'],  # Wx对应数据库中的Wx列
                    Wy=row['Wy']   # Wy对应数据库中的Wy列
                )
                sections.append(section)
            
            return sections
            
    def _get_sections_from_l_sections_2016_table(self, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从L_sections_2016表获取型钢截面数据
        
        Args:
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM L_sections_2016"
            params = []
            
            # 添加关键词搜索
            if keyword:
                query += " WHERE section_name LIKE ?"
                params.append(f"%{keyword}%")
            
            # 添加限制
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为SteelSection对象
            sections = []
            for row in rows:
                section = SteelSection(
                    shape_type="等边角钢截面表（2016）",  # 统一使用"等边角钢截面表（2016）"作为shape_type
                    model=row['section_name'],  # section_name作为model
                    side_width=row['side_width'],  # 边宽
                    edge_thickness=row['edge_thickness'],  # 边厚
                    round_radius=row['round_radius'],  # 使用数据库中的圆角半径
                    area=row['area'],
                    weight=row['weight'],
                    surface_area=row['surface_area'],  # 使用数据库中的表面积
                    Ix=row['Ix'],  # Ix对应数据库中的Ix列
                    Ix1=row['IX1'],  # IX1对应数据库中的IX1
                    Ix0=row['IX0'],  # IX0对应数据库中的IX0列    
                    Iy0=row['Iy0'],  # Iy0对应数据库中的Iy0列
                    ix=row['rx'],  # 惯性半径ix
                    ix0=row['rx0'],  # 惯性半径ix0
                    iy=row['ry0'],  # 惯性半径iy0
                    Wx=row['Wx'],  # wx对应数据库中的Wx列
                    Wy=row['Wy0'],  # wy对应数据库中的Wy0列
                    Wx0=row['WX0'],  # wx0对应数据库中的WX0列
                    Wy0=row['Wy0'],  # wy0对应数据库中的Wy0列
                    Z0=row['Z0']   # z0对应数据库中的Z0列
                )
                sections.append(section)
            
            return sections
            
    def _get_sections_from_non_l_sections_2016_table(self, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从non_L_sections_2016表获取型钢截面数据
        
        Args:
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM non_L_sections_2016"
            params = []
            
            # 添加关键词搜索
            if keyword:
                query += " WHERE section_name LIKE ?"
                params.append(f"%{keyword}%")
            
            # 添加限制
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为SteelSection对象
            sections = []
            for row in rows:
                section = SteelSection(
                    shape_type="不等边角钢截面表（2016）",  # 统一使用"不等边角钢截面表（2016）"作为shape_type
                    model=row['section_name'],  # section_name作为model
                    long_side_width=row['long_side_width'],  # 使用长边宽
                    short_side_width=row['short_side_width'],  # 使用短边宽
                    edge_thickness=row['edge_thickness'],  # 边厚
                    round_radius=row['round_radius'],  # 使用数据库中的圆角半径
                    area=row['area'],
                    weight=row['weight'],
                    surface_area=row['surface_area'],  # 使用数据库中的表面积
                    Ix=row['Ix'],  # Ix对应数据库中的Ix列
                    Ix1=row['Ix1'],  # Ix1对应数据库中的Ix1列
                    Iy=row['Iy'],  # Iy对应数据库中的Iy列
                    Iy1=row['Iy1'],  # Iy1对应数据库中的Iy1列
                    Iu=row['Iu'],  # Iu对应数据库中的Iu列
                    ix=row['rx'],  # 惯性半径ix
                    iy=row['ry'],  # 惯性半径iy
                    iu=row['ru'],  # 惯性半径ru
                    Wx=row['Wx'],  # wx对应数据库中的Wx列
                    Wy=row['Wy'],  # wy对应数据库中的Wy列
                    Wu=row['Wu'],  # Wu对应数据库中的Wu列
                    tan_theta=row['tan_theta'],  # 截面主轴夹角正切值
                )
                sections.append(section)
            
            return sections
            
    def _get_sections_from_c_sections_2016_table(self, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从c_sections_2016表获取型钢截面数据
        
        Args:
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM c_sections_2016"
            params = []
            
            # 添加关键词搜索
            if keyword:
                query += " WHERE section_name LIKE ?"
                params.append(f"%{keyword}%")
            
            # 添加限制
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # 转换为SteelSection对象
            sections = []
            for row in rows:
                section = SteelSection(
                    shape_type="C型钢截面表（2016）",  # 统一使用"C型钢截面表（2016）"作为shape_type
                    model=row['section_name'],  # section_name作为model
                    height=row['height'],
                    width=row['width'],
                    web_thickness=row['web_thickness'],  # 使用腹板厚度
                    flange_thickness=row['flange_thickness'],  # 使用翼缘厚度
                    round_radius=row['round_radius'],  # 使用数据库中的圆角半径
                    area=row['area'],
                    weight=row['weight'],
                    surface_area=row['surface_area'],  # 使用数据库中的表面积
                    Ix=row['Ix'],  # Ix对应数据库中的Ix列
                    Iy=row['Iy'],  # Iy对应数据库中的Iy列
                    ix=row['rx'],  # 惯性半径rx
                    iy=row['ry'],  # 惯性半径ry
                    Wx=row['Wx'],  # wx对应数据库中的Wx列
                    Wy=row['Wy']   # wy对应数据库中的Wy列
                )
                sections.append(section)
            
            return sections
    
    def get_sections(self, shape_type: str, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """获取指定类型的型钢截面列表
        
        Args:
            shape_type: 型钢类型
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        # 如果是H型钢2017系列，从h_sections_2017表获取数据
        # 检查是否为H型钢截面表（2017）格式，例如 "HW型钢截面表（2017）"
        if shape_type.endswith("型钢截面表（2017）"):
            
            # 检查是否有缓存且没有关键词搜索
            if not keyword and shape_type in self._cache:
                return self._cache[shape_type]
            
            # 从shape_type中提取类别（如从"HW型钢截面表（2017）"中提取"HW"）
            category = shape_type.split("型钢截面表（2017）")[0]
            
            # 从h_sections_2017表获取
            sections = self._get_sections_from_h_sections_table(category, keyword, limit)
            
            # 更新缓存（如果没有关键词搜索）
            if not keyword:
                self._cache[shape_type] = sections
                
            return sections
        # 如果是H型钢2024系列，从h_sections_2024表获取数据
        elif shape_type == "H型钢截面表（2024）":
            # 检查是否有缓存且没有关键词搜索
            if not keyword and shape_type in self._cache:
                return self._cache[shape_type]
            
            # 从h_sections_2024表获取
            sections = self._get_sections_from_h_sections_2024_table(keyword, limit)
            
            # 更新缓存（如果没有关键词搜索）
            if not keyword:
                self._cache[shape_type] = sections
                
            return sections
        # 如果是I型钢2016系列，从i_sections_2016表获取数据
        elif shape_type == "I型钢截面表（2016）":
            # 检查是否有缓存且没有关键词搜索
            if not keyword and shape_type in self._cache:
                return self._cache[shape_type]
            
            # 从i_sections_2016表获取
            sections = self._get_sections_from_i_sections_2016_table(keyword, limit)
            
            # 更新缓存（如果没有关键词搜索）
            if not keyword:
                self._cache[shape_type] = sections
                
            return sections
        # 如果是等边角钢2016系列，从L_sections_2016表获取数据
        elif shape_type == "等边角钢截面表（2016）":
            # 检查是否有缓存且没有关键词搜索
            if not keyword and shape_type in self._cache:
                return self._cache[shape_type]
            
            # 从L_sections_2016表获取
            sections = self._get_sections_from_l_sections_2016_table(keyword, limit)
            
            # 更新缓存（如果没有关键词搜索）
            if not keyword:
                self._cache[shape_type] = sections
                
            return sections
        # 如果是不等边角钢2016系列，从non_L_sections_2016表获取数据
        elif shape_type == "不等边角钢截面表（2016）":
            # 检查是否有缓存且没有关键词搜索
            if not keyword and shape_type in self._cache:
                return self._cache[shape_type]
            
            # 从non_L_sections_2016表获取
            sections = self._get_sections_from_non_l_sections_2016_table(keyword, limit)
            
            # 更新缓存（如果没有关键词搜索）
            if not keyword:
                self._cache[shape_type] = sections
                
            return sections
        # 如果是C型钢2016系列，从c_sections_2016表获取数据
        elif shape_type == "C型钢截面表（2016）":
            # 检查是否有缓存且没有关键词搜索
            if not keyword and shape_type in self._cache:
                return self._cache[shape_type]
            
            # 从c_sections_2016表获取
            sections = self._get_sections_from_c_sections_2016_table(keyword, limit)
            
            # 更新缓存（如果没有关键词搜索）
            if not keyword:
                self._cache[shape_type] = sections
                
            return sections
        
        # 默认返回空列表，确保总是返回可迭代对象
        return []

    def get_shape_types(self) -> List[str]:
        """获取所有型钢类型
        
        Returns:
            List[str]: 型钢类型列表
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            
            # 从sections表获取类型
            cursor.execute("SELECT DISTINCT shape_type FROM sections")
            rows = cursor.fetchall()
            types_from_sections = [row[0] for row in rows]
            
            # 从h_sections_2017表获取类型
            cursor.execute("SELECT DISTINCT category FROM h_sections_2017")
            rows = cursor.fetchall()
            types_from_h_sections = [f"{row[0]}型钢截面表（2017）" for row in rows]
            
            # 添加H型钢截面表（2024）类型
            types_from_h_sections_2024 = ["H型钢截面表（2024）"]
            
            # 添加I型钢截面表（2016）类型
            types_from_i_sections_2016 = ["I型钢截面表（2016）"]
            
            # 添加等边角钢截面表（2016）类型
            types_from_l_sections_2016 = ["等边角钢截面表（2016）"]
            
            # 添加不等边角钢截面表（2016）类型
            types_from_non_l_sections_2016 = ["不等边角钢截面表（2016）"]
            
            # 添加C型钢截面表（2016）类型
            types_from_c_sections_2016 = ["C型钢截面表（2016）"]
            
            # 合并七个列表
            all_types = types_from_sections + types_from_h_sections + types_from_h_sections_2024 + types_from_i_sections_2016 + types_from_l_sections_2016 + types_from_non_l_sections_2016 + types_from_c_sections_2016
            return all_types
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()