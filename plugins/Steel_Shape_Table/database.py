"""数据库操作模块"""

import sqlite3
import json
import os
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
    
    def _init_db(self):
        """初始化数据库，创建表结构"""
        # 确保数据库文件所在目录存在
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            # 创建sections表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    shape_type TEXT NOT NULL,
                    model TEXT NOT NULL,
                    height REAL NOT NULL,
                    width REAL NOT NULL,
                    web_thickness REAL NOT NULL,
                    flange_thickness REAL NOT NULL,
                    area REAL NOT NULL,
                    weight REAL NOT NULL,
                    ix REAL NOT NULL,
                    iy REAL NOT NULL,
                    wx REAL NOT NULL,
                    wy REAL NOT NULL,
                    UNIQUE(shape_type, model)
                )
            ''')
            conn.commit()
        
        # 初始化缓存
        self._load_cache()
    
    def _load_cache(self):
        """加载缓存"""
        # 获取所有型钢类型
        shape_types = self.get_shape_types()
        for shape_type in shape_types:
            # 预加载每种类型的前100条数据到缓存
            sections = self._get_sections_from_db(shape_type, limit=100)
            self._cache[shape_type] = sections
    
    def _get_sections_from_db(self, shape_type: str, keyword: str = None, limit: int = None) -> List[SteelSection]:
        """从数据库获取型钢截面数据
        
        Args:
            shape_type: 型钢类型
            keyword: 搜索关键词
            limit: 限制返回数量
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询语句
            query = "SELECT * FROM sections WHERE shape_type = ?"
            params = [shape_type]
            
            # 添加关键词搜索
            if keyword:
                query += " AND model LIKE ?"
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
                    shape_type=row['shape_type'],
                    model=row['model'],
                    height=row['height'],
                    width=row['width'],
                    web_thickness=row['web_thickness'],
                    flange_thickness=row['flange_thickness'],
                    area=row['area'],
                    weight=row['weight'],
                    ix=row['ix'],
                    iy=row['iy'],
                    wx=row['wx'],
                    wy=row['wy']
                )
                sections.append(section)
            
            return sections
    
    def get_sections(self, shape_type: str, keyword: str = None) -> List[SteelSection]:
        """获取指定类型的型钢截面列表
        
        Args:
            shape_type: 型钢类型
            keyword: 搜索关键词
            
        Returns:
            List[SteelSection]: 型钢截面列表
        """
        # 检查是否有缓存且没有关键词搜索
        if not keyword and shape_type in self._cache:
            return self._cache[shape_type]
        
        # 从数据库获取
        sections = self._get_sections_from_db(shape_type, keyword)
        
        # 更新缓存（如果没有关键词搜索）
        if not keyword:
            self._cache[shape_type] = sections
        
        return sections
    
    def get_shape_types(self) -> List[str]:
        """获取所有型钢类型
        
        Returns:
            List[str]: 型钢类型列表
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT shape_type FROM sections")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    
    def add_section(self, section: SteelSection) -> bool:
        """添加型钢截面数据
        
        Args:
            section: 型钢截面对象
            
        Returns:
            bool: 是否添加成功
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO sections (
                        shape_type, model, height, width, web_thickness, 
                        flange_thickness, area, weight, ix, iy, wx, wy
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    section.shape_type, section.model, section.height, section.width, 
                    section.web_thickness, section.flange_thickness, section.area, 
                    section.weight, section.ix, section.iy, section.wx, section.wy
                ))
                conn.commit()
            
            # 更新缓存
            if section.shape_type in self._cache:
                # 检查是否已存在
                existing = next((s for s in self._cache[section.shape_type] if s.model == section.model), None)
                if existing:
                    # 替换现有数据
                    self._cache[section.shape_type].remove(existing)
                self._cache[section.shape_type].append(section)
            
            return True
        except Exception as e:
            print(f"添加截面失败: {e}")
            return False
    
    def add_sections(self, sections: List[SteelSection]) -> int:
        """批量添加型钢截面数据
        
        Args:
            sections: 型钢截面对象列表
            
        Returns:
            int: 成功添加的数量
        """
        count = 0
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            for section in sections:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO sections (
                            shape_type, model, height, width, web_thickness, 
                            flange_thickness, area, weight, ix, iy, wx, wy
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        section.shape_type, section.model, section.height, section.width, 
                        section.web_thickness, section.flange_thickness, section.area, 
                        section.weight, section.ix, section.iy, section.wx, section.wy
                    ))
                    count += 1
                except Exception as e:
                    print(f"添加截面 {section.model} 失败: {e}")
            conn.commit()
        
        # 清空缓存，下次查询时重新加载
        self._cache.clear()
        
        return count
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
    
    def backup_to_json(self, json_path: str) -> bool:
        """备份数据库到JSON文件
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            bool: 是否备份成功
        """
        try:
            # 获取所有数据
            all_sections = []
            shape_types = self.get_shape_types()
            for shape_type in shape_types:
                sections = self.get_sections(shape_type)
                all_sections.extend(sections)
            
            # 转换为字典列表
            sections_dict = {
                "sections": [section.to_dict() for section in all_sections]
            }
            
            # 写入JSON文件
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sections_dict, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"备份到JSON失败: {e}")
            return False
    
    def restore_from_json(self, json_path: str) -> int:
        """从JSON文件恢复数据库
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            int: 成功恢复的数量
        """
        try:
            # 读取JSON文件
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 转换为SteelSection对象
            sections = [SteelSection.from_dict(section_dict) for section_dict in data.get('sections', [])]
            
            # 批量添加到数据库
            return self.add_sections(sections)
        except Exception as e:
            print(f"从JSON恢复失败: {e}")
            return 0
