"""数据导入工具"""

import os
import json
from plugins.Steel_Shape_Table.database import SectionDatabase
from plugins.Steel_Shape_Table.models import SteelSection


class DataImporter:
    """数据导入工具类"""
    
    def __init__(self, db_path: str):
        """初始化数据导入工具
        
        Args:
            db_path: 数据库文件路径
        """
        self._db = SectionDatabase(db_path)
    
    def import_from_json(self, json_path: str) -> int:
        """从JSON文件导入数据到数据库
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            int: 成功导入的记录数
        """
        try:
            # 读取JSON文件
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 转换为SteelSection对象列表
            sections = []
            for section_dict in data.get('sections', []):
                section = SteelSection.from_dict(section_dict)
                sections.append(section)
            
            # 批量导入到数据库
            return self._db.add_sections(sections)
        except Exception as e:
            print(f"从JSON导入失败: {e}")
            return 0
    
    def export_to_json(self, json_path: str) -> bool:
        """将数据库数据导出到JSON文件
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            bool: 是否导出成功
        """
        return self._db.backup_to_json(json_path)
    
    def update_from_json(self, json_path: str) -> int:
        """从JSON文件更新数据库数据（仅更新已存在的记录）
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            int: 成功更新的记录数
        """
        try:
            # 读取JSON文件
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 转换为SteelSection对象列表
            sections = []
            for section_dict in data.get('sections', []):
                section = SteelSection.from_dict(section_dict)
                sections.append(section)
            
            # 更新到数据库
            updated_count = 0
            for section in sections:
                if self._db.add_section(section):
                    updated_count += 1
            
            return updated_count
        except Exception as e:
            print(f"从JSON更新失败: {e}")
            return 0


def initialize_database():
    """初始化数据库，从JSON文件导入初始数据"""
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 数据库文件路径
    db_path = os.path.join(current_dir, 'sections.db')
    
    # JSON文件路径
    json_path = os.path.join(current_dir, 'sections.json')
    
    # 创建数据导入工具
    importer = DataImporter(db_path)
    
    # 从JSON文件导入数据
    imported_count = importer.import_from_json(json_path)
    print(f"成功导入 {imported_count} 条记录到数据库")
    
    return imported_count


if __name__ == '__main__':
    # 执行数据库初始化
    initialize_database()