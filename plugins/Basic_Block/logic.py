"""块式基础计算插件业务逻辑"""


class BasicBlockLogic:
    """块式基础计算插件业务逻辑"""
    
    def __init__(self):
        """初始化业务逻辑"""
        pass
    
    def calculate_basic_volume(self, length, width, height):
        """计算基础体积
        
        Args:
            length: 基础长度 (m)
            width: 基础宽度 (m)
            height: 基础高度 (m)
            
        Returns:
            基础体积 (m³)
        """
        return length * width * height
    
    def calculate_cushion_volume(self, length, width, cushion_thickness):
        """计算垫层体积
        
        Args:
            length: 基础长度 (m)
            width: 基础宽度 (m)
            cushion_thickness: 垫层厚度 (m)
            
        Returns:
            垫层体积 (m³)
        """
        # 假设100是mm，转换为0.1m，每边增加0.1m，所以总共增加2*0.1m
        return (length + 2 * 0.1) * (width + 2 * 0.1) * cushion_thickness
    
    def calculate_replacement_volume(self, length, width, replacement_width, replacement_thickness):
        """计算换填级配砂石体积
        
        Args:
            length: 基础长度 (m)
            width: 基础宽度 (m)
            replacement_width: 换填宽度 (m)
            replacement_thickness: 换填厚度 (m)
            
        Returns:
            换填级配砂石体积 (m³)
        """
        # 单个基础换填级配砂石体积=（基础长度+2*换填宽度）*（基础宽度+2*换填宽度）*换填厚度
        return (length + 2 * replacement_width) * (width + 2 * replacement_width) * replacement_thickness
    
    def calculate_anchor_bolt_volume(self, diameter, length):
        """计算单根地脚螺栓的体积
        
        Args:
            diameter: 地脚螺栓直径 (mm)
            length: 地脚螺栓长度 (mm)
            
        Returns:
            单根地脚螺栓体积 (m³)
        """
        # 将直径和长度转换为米
        diameter_m = diameter / 1000
        length_m = length / 1000
        # 计算体积：π * (d/2)² * h
        import math
        return math.pi * (diameter_m / 2) ** 2 * length_m
    
    def calculate_steel_weight(self, anchor_bolt_volume, anchor_bolt_count):
        """计算钢材重量
        
        Args:
            anchor_bolt_volume: 单根地脚螺栓体积 (m³)
            anchor_bolt_count: 地脚螺栓个数
            
        Returns:
            钢材重量 (kg)
        """
        # 钢材密度：7850 kg/m³
        steel_density = 7850
        return anchor_bolt_volume * anchor_bolt_count * steel_density
    
    def check_bearing_capacity(self, upper_load, length, width, height, bearing_capacity, is_plain_concrete=False):
        """验算地基承载力是否满足要求
        
        Args:
            upper_load: 上部荷载 (KN)
            length: 基础长度 (m)
            width: 基础宽度 (m)
            height: 基础高度 (m)
            bearing_capacity: 地基承载力 (kPa)
            is_plain_concrete: 是否素砼，默认否
            
        Returns:
            tuple: (是否满足要求, 基础自重, 总荷载, 基底压力, 基础密度)
        """
        # 根据是否素砼选择基础密度
        # 素砼：22 KN/m³，否则：25 KN/m³
        concrete_density = 22 if is_plain_concrete else 25
        
        # 计算基础体积 (m³)
        basic_volume = length * width * height
        
        # 计算基础自重 (KN)
        basic_weight = basic_volume * concrete_density
        
        # 计算总荷载 (KN)
        total_load = upper_load + basic_weight
        
        # 计算基底面积 (m²)
        base_area = length * width
        
        # 计算基底压力 (kPa)
        base_pressure = total_load / base_area
        
        # 验算地基承载力
        is_satisfied = base_pressure <= bearing_capacity
        
        return is_satisfied, basic_weight, total_load, base_pressure, concrete_density
    
    def calculate_anticorrosion_area(self, length, width, depth):
        """计算基础防腐面积
        
        Args:
            length: 基础长度 (m)
            width: 基础宽度 (m)
            depth: 基底埋深 (m)
            
        Returns:
            基础防腐面积 (m²)
        """
        # 基础防腐面积 = 基础侧面积 = (长度 + 宽度) × 2 × 高度（基底埋深）
        return (length + width) * 2 * depth
    
    def calculate_grout_volume(self, length, width, grout_thickness):
        """计算二次灌浆体积
        
        Args:
            length: 基础长度 (m)
            width: 基础宽度 (m)
            grout_thickness: 二次灌浆厚度 (mm)，需要转换为米
            
        Returns:
            二次灌浆体积 (m³)
        """
        # 将二次灌浆厚度从mm转换为m
        grout_thickness_m = grout_thickness / 1000
        # 二次灌浆体积 = 基础长 * 基础宽 * 二次灌浆层厚度
        return length * width * grout_thickness_m
    
    def calculate_plate_volume(self, plate_length, plate_width, plate_thickness):
        """计算预埋钢板体积
        
        Args:
            plate_length: 预埋钢板长度 (m)
            plate_width: 预埋钢板宽度 (m)
            plate_thickness: 预埋钢板厚度 (mm)，需要转换为米
            
        Returns:
            预埋钢板体积 (m³)
        """
        # 将预埋钢板厚度从mm转换为m
        plate_thickness_m = plate_thickness / 1000
        # 预埋钢板体积 = 长度 * 宽度 * 厚度
        return plate_length * plate_width * plate_thickness_m
