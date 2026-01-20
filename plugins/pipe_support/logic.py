"""管墩计算插件业务逻辑"""


class PipeSupportLogic:
    """管墩计算插件业务逻辑"""
    
    def __init__(self):
        """初始化业务逻辑"""
        pass
    
    def calculate_basic_volume(self, base_length, base_bottom_width, base_top_width, base_height, base_column_length, base_column_width, base_plate_height, foundation_style):
        """计算基础体积
        
        Args:
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            base_top_width: 基础顶面宽度 (m)
            base_height: 基础高度 (m)
            base_column_length: 基础短柱长度 (m)
            base_column_width: 基础短柱宽度 (m)
            base_plate_height: 底板高度 (m)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            
        Returns:
            基础体积 (m³)
        """
        if foundation_style == "T型基础":
            # T型基础体积 = 底板体积 + 短柱体积
            # 底板体积 = 底板长度 × 底板宽度 × 底板高度
            # 短柱体积 = 基础短柱长度 × 基础短柱宽度 × (基础高度 - 底板高度)
            base_plate_volume = base_length * base_bottom_width * base_plate_height
            column_volume = base_column_length * base_column_width * (base_height - base_plate_height)
            return base_plate_volume + column_volume
        else:
            # 梯形基础体积 = （底板宽度+基础顶面宽度）*基础高度/2*底板长度
            return (base_bottom_width + base_top_width) * base_height / 2 * base_length
    
    def calculate_cushion_volume(self, base_length, base_bottom_width, cushion_thickness, foundation_style):
        """计算垫层体积
        
        Args:
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            cushion_thickness: 垫层厚度 (m)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            
        Returns:
            垫层体积 (m³)
        """
        if foundation_style == "T型基础":
            # T型基础垫层体积=（底板长度+2*0.1）*（底板宽度+2*0.1）*垫层厚度
            return (base_length + 2 * 0.1) * (base_bottom_width + 2 * 0.1) * cushion_thickness
        else:
            # 梯形基础垫层体积=（底板长度+2*0.1）*（底板宽度+2*0.1）*垫层厚度
            return (base_length + 2 * 0.1) * (base_bottom_width + 2 * 0.1) * cushion_thickness
    
    def calculate_replacement_volume(self, base_length, base_bottom_width, replacement_width, replacement_thickness, foundation_style):
        """计算换填级配砂石体积
        
        Args:
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            replacement_width: 换填宽度 (m)
            replacement_thickness: 换填厚度 (m)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            
        Returns:
            换填级配砂石体积 (m³)
        """
        if foundation_style == "T型基础":
            # T型基础换填级配砂石体积 = (底板长度 + 2 * 换填级配砂石宽度) × (底板宽度 + 2 * 换填级配砂石宽度) × 换填级配砂石厚度
            return (base_length + 2 * replacement_width) * (base_bottom_width + 2 * replacement_width) * replacement_thickness
        else:
            # 梯形基础换填级配砂石体积 = (底板长度 + 2 * 换填级配砂石宽度) × (底板宽度 + 2 * 换填级配砂石宽度) × 换填级配砂石厚度
            return (base_length + 2 * replacement_width) * (base_bottom_width + 2 * replacement_width) * replacement_thickness
    
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
    
    def calculate_grout_volume(self, base_length, base_bottom_width, grout_thickness, base_column_length, base_column_width, foundation_style):
        """计算二次灌浆体积
        
        Args:
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            grout_thickness: 二次灌浆厚度 (mm)，需要转换为米
            base_column_length: 基础短柱长度 (m)
            base_column_width: 基础短柱宽度 (m)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            
        Returns:
            二次灌浆体积 (m³)
        """
        # 将二次灌浆厚度从mm转换为m
        grout_thickness_m = grout_thickness / 1000
        
        if foundation_style == "T型基础":
            # T型基础二次灌浆体积 = 短柱长度 * 短柱宽度 * 二次灌浆层厚度
            return base_column_length * base_column_width * grout_thickness_m
        else:
            # 梯形基础二次灌浆体积 = 基础长 * 基础宽 * 二次灌浆层厚度
            return base_length * base_bottom_width * grout_thickness_m
    

    
    def calculate_anticorrosion_area(self, base_length, base_bottom_width, depth, base_column_length, base_column_width, base_plate_height, foundation_style, base_top_width=0):
        """计算基础防腐面积
        
        Args:
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            depth: 基底埋深 (m)
            base_column_length: 基础短柱长度 (m)
            base_column_width: 基础短柱宽度 (m)
            base_plate_height: 底板高度 (m)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            base_top_width: 基础顶面宽度 (m)，仅梯形基础使用
            
        Returns:
            基础防腐面积 (m²)
        """
        if foundation_style == "T型基础":
            # T型基础防腐面积 = 底板侧面积 + 短柱侧面积（埋入地下部分）
            # 底板侧面积 = (底板长 + 底板宽) × 2 × 底板高度
            # 短柱侧面积 = (基础短柱长度 + 基础短柱宽度) × 2 × (基础高度 - 底板高度 - 基础高出底面高度)
            # 注意：基础高出底面高度 = 基础高度 - 基底埋深
            base_plate_area = (base_length + base_bottom_width) * 2 * base_plate_height
            column_buried_height = depth - base_plate_height  # 短柱埋入地下高度
            if column_buried_height > 0:
                column_area = (base_column_length + base_column_width) * 2 * column_buried_height
            else:
                column_area = 0
            return base_plate_area + column_area
        else:
            # 梯形基础防腐面积 = 2个梯形侧面 + 2个矩形侧面
            # 单个梯形侧面积 = （基础顶面宽度+底板宽度）*基础高度/2
            # 单个矩形侧面积 = √（基础高度² + （( 底板宽度 − 基础顶面宽度 )/2）²）*底板长度
            import math
            # 计算梯形侧面面积（2个）
            trapezoid_area = 2 * (base_top_width + base_bottom_width) * depth / 2
            # 计算矩形侧面面积（2个）
            slant_height = math.sqrt(depth ** 2 + ((base_bottom_width - base_top_width) / 2) ** 2)
            rectangle_area = 2 * slant_height * base_length
            return trapezoid_area + rectangle_area

    def check_bearing_capacity(self, upper_load, base_length, base_bottom_width, base_height, bearing_capacity, foundation_style, base_column_length=0, base_column_width=0, base_plate_height=0):
        """验算地基承载力是否满足要求
        
        Args:
            upper_load: 上部荷载 (KN)
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            base_height: 基础高度 (m)
            bearing_capacity: 地基承载力 (kPa)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            base_column_length: 基础短柱长度 (m)，仅T型基础使用
            base_column_width: 基础短柱宽度 (m)，仅T型基础使用
            base_plate_height: 底板高度 (m)，仅T型基础使用
            
        Returns:
            tuple: (是否满足要求, 基础自重, 总荷载, 基底压力, 基础密度)
        """
        # 混凝土密度：25 KN/m³
        concrete_density = 25
        
        if foundation_style == "T型基础":
            # T型基础体积 = 底板体积 + 短柱体积
            base_plate_volume = base_length * base_bottom_width * base_plate_height
            column_volume = base_column_length * base_column_width * (base_height - base_plate_height)
            basic_volume = base_plate_volume + column_volume
            # 基底面积 = 底板长度 × 底板宽度
            base_area = base_length * base_bottom_width
        else:
            # 梯形基础体积 = （底板宽度+基础顶面宽度）*基础高度/2*底板长度
            # 这里简化处理，使用底板面积作为基底面积
            basic_volume = base_length * base_bottom_width * base_height
            base_area = base_length * base_bottom_width
        
        # 计算基础自重 (KN)
        basic_weight = basic_volume * concrete_density
        
        # 计算总荷载 (KN)
        total_load = upper_load + basic_weight
        
        # 计算基底压力 (kPa)
        base_pressure = total_load / base_area
        
        # 验算地基承载力
        is_satisfied = base_pressure <= bearing_capacity
        
        return is_satisfied, basic_weight, total_load, base_pressure, concrete_density