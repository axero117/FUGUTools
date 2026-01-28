"""型钢特性表业务逻辑"""

import os
from plugins.Steel_Shape_Table.database import SectionDatabase
from plugins.Steel_Shape_Table.data.import_tools import initialize_database


class SteelShapeLogic:
    """型钢特性表业务逻辑"""
    
    def __init__(self):
        """初始化业务逻辑"""
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 数据库文件路径
        self._db_path = os.path.join(current_dir, 'data', 'sections.db')
        
        # 初始化数据库（如果数据库不存在或为空，则从JSON导入数据）
        self._init_database()
        
        # 创建数据库连接
        self._db = SectionDatabase(self._db_path)
    
    def _init_database(self):
        """初始化数据库"""
        # 检查数据库文件是否存在且大小大于0
        if not os.path.exists(self._db_path) or os.path.getsize(self._db_path) == 0:
            # 初始化数据库，从JSON文件导入数据
            initialize_database()
    
    def get_steel_shapes(self, shape_type, keyword=None):
        """获取指定类型的型钢列表
        
        Args:
            shape_type: 型钢类型（如"H型钢"、"工字钢"等）
            keyword: 搜索关键词
            
        Returns:
            list: 型钢列表，每个元素为字典，使用中文键名
        """
        sections = self._db.get_sections(shape_type, keyword)
        
        # 转换为字典列表，使用数据库列名作为键
        result = []
        for section in sections:
            section_dict = section.to_dict()
            result.append(section_dict)
        return result
    
    def get_shape_types(self):
        """获取所有型钢类型
        
        Returns:
            list: 型钢类型列表
        """
        return self._db.get_shape_types()
    
    def search_shapes(self, shape_type, keyword):
        """根据关键词搜索型钢
        
        Args:
            shape_type: 型钢类型
            keyword: 搜索关键词
            
        Returns:
            list: 匹配的型钢列表，每个元素为字典，使用中文键名
        """
        return self.get_steel_shapes(shape_type, keyword)
    
    def add_section(self, section_dict):
        """添加型钢截面数据
        
        Args:
            section_dict: 型钢截面数据字典
            
        Returns:
            bool: 是否添加成功
        """
        from plugins.Steel_Shape_Table.models import SteelSection
        # 转换为英文键名
        english_dict = {
            "shape_type": section_dict.get("shape_type"),
            "model": section_dict.get("型号"),
            "height": section_dict.get("高度H"),
            "width": section_dict.get("宽度B"),
            "web_thickness": section_dict.get("腹板厚度t1"),
            "flange_thickness": section_dict.get("翼缘厚度t2"),
            "fillet_radius": section_dict.get("圆角半径r"),
            "inner_fillet_radius": section_dict.get("内圆角半径r'"),
            "area": section_dict.get("截面面积"),
            "weight": section_dict.get("理论重量"),
            "surface_area": section_dict.get("表面积"),
            "ix": section_dict.get("惯性矩Ix"),
            "iy": section_dict.get("惯性矩Iy"),
            "rx": section_dict.get("惯性半径rx"),
            "ry": section_dict.get("惯性半径ry"),
            "wx": section_dict.get("截面模量Wx"),
            "wy": section_dict.get("截面模量Wy")
        }
        section = SteelSection.from_dict(english_dict)
        return self._db.add_section(section)
    
    def backup_database(self, json_path):
        """备份数据库到JSON文件
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            bool: 是否备份成功
        """
        return self._db.backup_to_json(json_path)
    
    def restore_database(self, json_path):
        """从JSON文件恢复数据库
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            int: 成功恢复的记录数
        """
        return self._db.restore_from_json(json_path)