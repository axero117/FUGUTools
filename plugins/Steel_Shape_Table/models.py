"""型钢数据模型"""


class SteelSection:
    """型钢截面模型"""
    
    def __init__(self, shape_type=None, model=None, height=0, width=0, web_thickness=0,
                 flange_thickness=0, fillet_radius=0, inner_fillet_radius=0, area=0, 
                 weight=0, surface_area=0, Ix=0, Iy=0, Ix1=0, Ix0=0, Iy0=0, Iy1=0, Iu=0, ix=0, iy=0, ix0=0, iu=0, rx=0, ry=0, rx0=0, ru=0, 
                 Wx=0, Wy=0, Wx0=0, Wy0=0, Wu=0, Z0=0, category=None, side_width=0, edge_thickness=0, round_radius=0, 
                 long_side_width=0, short_side_width=0, tan_theta=0):
        """初始化型钢截面模型
        
        Args:
            shape_type: 型钢类型（如"H型钢"、"工字钢"等）
            model: 型号
            height: 高度(mm)
            width: 宽度(mm)
            web_thickness: 腹板厚度(mm)
            flange_thickness: 翼缘厚度(mm)
            fillet_radius: 圆角半径(mm)
            inner_fillet_radius: 内圆角半径(mm)
            area: 截面面积(cm²)
            weight: 理论重量(kg/m)
            surface_area: 表面积(m²/m)
            Ix: 惯性矩Ix(cm⁴)
            Iy: 惯性矩Iy(cm⁴)
            Ix1: 惯性矩IX1(cm⁴)
            Ix0: 惯性矩IX0(cm⁴)
            Iy0: 惯性矩Iy0(cm⁴)
            Iy1: 惯性矩Iy1(cm⁴)
            Iu: 惯性矩Iu(cm⁴)
            ix: 惯性半径ix(cm)
            iy: 惯性半径iy(cm)
            ix0: 惯性半径ix0(cm)
            iu: 惯性半径iu(cm)
            rx: 惯性半径rx(cm)
            ry: 惯性半径ry(cm)
            rx0: 惯性半径rx0(cm)
            ru: 惯性半径ru(cm)
            Wx: 截面模量Wx(cm³)
            Wy: 截面模量Wy(cm³)
            Wx0: 截面模量WX0(cm³)
            Wy0: 截面模量Wy0(cm³)
            Wu: 截面模量Wu(cm³)
            Z0: 重心距离Z0(cm)
            category: 型钢类别 (HW/HM/HN/HP等)
            side_width: 边宽(mm)
            edge_thickness: 边厚(mm)
            round_radius: 圆角半径(mm)
            long_side_width: 长边宽(mm)
            short_side_width: 短边宽(mm)
            tan_theta: 主惯性轴偏转角度的正切值
        """
        self.shape_type = shape_type
        self.model = model
        self.height = height
        self.width = width
        self.web_thickness = web_thickness
        self.flange_thickness = flange_thickness
        self.fillet_radius = fillet_radius
        self.inner_fillet_radius = inner_fillet_radius
        self.area = area
        self.weight = weight
        self.surface_area = surface_area
        self.Ix = Ix
        self.Iy = Iy
        self.Ix1 = Ix1
        self.Ix0 = Ix0
        self.Iy0 = Iy0
        self.Iy1 = Iy1
        self.Iu = Iu
        self.ix = ix
        self.iy = iy
        self.ix0 = ix0
        self.iu = iu
        self.rx = rx
        self.ry = ry
        self.rx0 = rx0
        self.ru = ru
        self.Wx = Wx
        self.Wy = Wy
        self.Wx0 = Wx0
        self.Wy0 = Wy0
        self.Wu = Wu
        self.Z0 = Z0
        self.category = category
        self.side_width = side_width
        self.edge_thickness = edge_thickness
        self.round_radius = round_radius
        self.long_side_width = long_side_width
        self.short_side_width = short_side_width
        self.tan_theta = tan_theta
    
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
            'fillet_radius': self.fillet_radius,
            'inner_fillet_radius': self.inner_fillet_radius,
            'area': self.area,
            'weight': self.weight,
            'surface_area': self.surface_area,
            'Ix': self.Ix,
            'Iy': self.Iy,
            'Ix1': self.Ix1,
            'Ix0': self.Ix0,
            'Iy0': self.Iy0,
            'Iy1': self.Iy1,
            'Iu': self.Iu,
            'ix': self.ix,
            'iy': self.iy,
            'ix0': self.ix0,
            'iu': self.iu,
            'rx': self.rx,
            'ry': self.ry,
            'rx0': self.rx0,
            'ru': self.ru,
            'Wx': self.Wx,
            'Wy': self.Wy,
            'Wx0': self.Wx0,
            'Wy0': self.Wy0,
            'Wu': self.Wu,
            'Z0': self.Z0,
            'category': self.category,
            'side_width': self.side_width,
            'edge_thickness': self.edge_thickness,
            'round_radius': self.round_radius,
            'long_side_width': self.long_side_width,
            'short_side_width': self.short_side_width,
            'tan_theta': self.tan_theta
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
            fillet_radius=data_dict.get('fillet_radius', 0),
            inner_fillet_radius=data_dict.get('inner_fillet_radius', 0),
            area=data_dict.get('area', 0),
            weight=data_dict.get('weight', 0),
            surface_area=data_dict.get('surface_area', 0),
            Ix=data_dict.get('Ix', 0),
            Iy=data_dict.get('Iy', 0),
            Ix1=data_dict.get('Ix1', 0),
            Ix0=data_dict.get('Ix0', 0),
            Iy0=data_dict.get('Iy0', 0),
            Iy1=data_dict.get('Iy1', 0),
            Iu=data_dict.get('Iu', 0),
            ix=data_dict.get('ix', 0),
            iy=data_dict.get('iy', 0),
            ix0=data_dict.get('ix0', 0),
            iu=data_dict.get('iu', 0),
            rx=data_dict.get('rx', 0),
            ry=data_dict.get('ry', 0),
            rx0=data_dict.get('rx0', 0),
            ru=data_dict.get('ru', 0),
            Wx=data_dict.get('Wx', 0),
            Wy=data_dict.get('Wy', 0),
            Wx0=data_dict.get('Wx0', 0),
            Wy0=data_dict.get('Wy0', 0),
            Wu=data_dict.get('Wu', 0),
            Z0=data_dict.get('Z0', 0),
            category=data_dict.get('category'),
            side_width=data_dict.get('side_width', 0),
            edge_thickness=data_dict.get('edge_thickness', 0),
            round_radius=data_dict.get('round_radius', 0),
            long_side_width=data_dict.get('long_side_width', 0),
            short_side_width=data_dict.get('short_side_width', 0),
            tan_theta=data_dict.get('tan_theta', 0)
        )
    
    def __str__(self):
        """字符串表示
        
        Returns:
            str: 型钢截面的字符串表示
        """
        return f"{self.shape_type} {self.model}"