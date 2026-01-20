"""型钢数据模型"""


class SteelSection:
    """型钢截面模型"""
    
    def __init__(self, shape_type=None, model=None, height=0, width=0, web_thickness=0,
                 flange_thickness=0, area=0, weight=0, ix=0, iy=0, wx=0, wy=0):
        """初始化型钢截面模型
        
        Args:
            shape_type: 型钢类型（如"H型钢"、"工字钢"等）
            model: 型号
            height: 高度(mm)
            width: 宽度(mm)
            web_thickness: 腹板厚度(mm)
            flange_thickness: 翼缘厚度(mm)
            area: 截面面积(cm²)
            weight: 理论重量(kg/m)
            ix: 惯性矩Ix(cm⁴)
            iy: 惯性矩Iy(cm⁴)
            wx: 截面模量Wx(cm³)
            wy: 截面模量Wy(cm³)
        """
        self.shape_type = shape_type
        self.model = model
        self.height = height
        self.width = width
        self.web_thickness = web_thickness
        self.flange_thickness = flange_thickness
        self.area = area
        self.weight = weight
        self.ix = ix
        self.iy = iy
        self.wx = wx
        self.wy = wy
    
    def to_dict(self):
        """转换为字典格式
        
        Returns:
            dict: 型钢截面数据字典
        """
        return {
            'shape_type': self.shape_type,
            'model': self.model,
            'height': self.height,
            'width': self.width,
            'web_thickness': self.web_thickness,
            'flange_thickness': self.flange_thickness,
            'area': self.area,
            'weight': self.weight,
            'ix': self.ix,
            'iy': self.iy,
            'wx': self.wx,
            'wy': self.wy
        }
    
    @classmethod
    def from_dict(cls, data_dict):
        """从字典创建型钢截面模型
        
        Args:
            data_dict: 型钢截面数据字典
            
        Returns:
            SteelSection: 型钢截面模型实例
        """
        return cls(
            shape_type=data_dict.get('shape_type'),
            model=data_dict.get('model'),
            height=data_dict.get('height', 0),
            width=data_dict.get('width', 0),
            web_thickness=data_dict.get('web_thickness', 0),
            flange_thickness=data_dict.get('flange_thickness', 0),
            area=data_dict.get('area', 0),
            weight=data_dict.get('weight', 0),
            ix=data_dict.get('ix', 0),
            iy=data_dict.get('iy', 0),
            wx=data_dict.get('wx', 0),
            wy=data_dict.get('wy', 0)
        )
    
    def __str__(self):
        """字符串表示
        
        Returns:
            str: 型钢截面的字符串表示
        """
        return f"{self.shape_type} {self.model}"
