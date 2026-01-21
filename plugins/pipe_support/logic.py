"""管墩计算插件业务逻辑"""

import math


class PipeSupportLogic:
    """管墩计算插件业务逻辑"""
    
    # 常量定义
    CONCRETE_DENSITY = 25  # 混凝土密度：25 KN/m³
    SOIL_DENSITY = 18  # 覆土重度：18 KN/m³
    GROUNDWATER_SOIL_DENSITY = 10  # 考虑地下水时覆土重度：10 KN/m³
    
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
        # 垫层体积=（底板长度+2*0.1）*（底板宽度+2*0.1）*垫层厚度
        # 两种基础样式的计算方式相同
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
        # 换填级配砂石体积 = (底板长度 + 2 * 换填级配砂石宽度) × (底板宽度 + 2 * 换填级配砂石宽度) × 换填级配砂石厚度
        # 两种基础样式的计算方式相同
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
            # 计算梯形侧面面积（2个）
            trapezoid_area = 2 * (base_top_width + base_bottom_width) * depth / 2
            # 计算矩形侧面面积（2个）
            slant_height = math.sqrt(depth ** 2 + ((base_bottom_width - base_top_width) / 2) ** 2)
            rectangle_area = 2 * slant_height * base_length
            return trapezoid_area + rectangle_area

    def check_bearing_capacity(self, upper_load, base_length, base_bottom_width, base_height, bearing_capacity, foundation_style, base_column_length=0, base_column_width=0, base_plate_height=0, base_height_above_ground=0, upper_horizontal_load=0, consider_groundwater="否", base_top_width=0):
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
            base_height_above_ground: 基础高出地面高度 (m)，仅T型基础使用
            upper_horizontal_load: 上部水平荷载 (KN)，用于计算基底弯矩
            consider_groundwater: 是否考虑地下水 ("是" 或 "否")
            base_top_width: 基础顶面宽度 (m)，仅梯形基础使用

        Returns:
            tuple: (是否满足要求, 基础自重, 覆土荷载, 总荷载, 基底压力, 基础密度, pkmax, pkmin, base_moment, section_modulus)
        """
        # 覆土重度：18 KN/m³（考虑地下水时为10 KN/m³）
        soil_density = self.GROUNDWATER_SOIL_DENSITY if consider_groundwater == "是" else self.SOIL_DENSITY
        
        # 初始化新计算参数
        pkmax = 0
        pkmin = 0
        base_moment = 0
        section_modulus = 0
        
        if foundation_style == "T型基础":
            # 使用 calculate_basic_volume 函数计算基础体积
            basic_volume = self.calculate_basic_volume(
                base_length, base_bottom_width, 0, base_height, 
                base_column_length, base_column_width, base_plate_height, foundation_style
            )
            # 基底面积 = 底板长度 × 底板宽度
            base_area = base_length * base_bottom_width
            
            # 计算覆土荷载
            # 覆土荷载=覆土重度18kN/m³*（底板面积-短柱面积）*（基础高度-基础高出地面高度-底板高度）
            # 计算基底埋深：基础高度减去基础高出地面高度
            depth = base_height - base_height_above_ground
            # 计算覆土高度：基底埋深减去底板高度
            soil_height = depth - base_plate_height
            
            # 计算底板面积和短柱面积
            base_plate_area = base_length * base_bottom_width
            column_area = base_column_length * base_column_width
            
            # 计算覆土荷载
            if soil_height > 0:
                soil_load = soil_density * (base_plate_area - column_area) * soil_height
            else:
                soil_load = 0
        else:
            # 使用 calculate_basic_volume 函数计算梯形基础体积，传入 base_top_width
            basic_volume = self.calculate_basic_volume(
                base_length, base_bottom_width, base_top_width, base_height, 
                0, 0, 0, foundation_style
            )
            base_area = base_length * base_bottom_width
            # 梯形基础暂不计算覆土荷载
            soil_load = 0
        
        # 计算基础自重 (KN)
        basic_weight = basic_volume * self.CONCRETE_DENSITY
        
        # 计算总荷载 (KN)
        total_load = upper_load + basic_weight + soil_load
        
        # 计算基底压力 (kPa)
        base_pressure = total_load / base_area
        
        # 计算基底弯矩和截面抵抗矩（仅T型基础）
        if foundation_style == "T型基础":
            if upper_horizontal_load > 0:
                # 基底弯矩 = 水平荷载 × 作用高度 (kN·m)
                base_moment = upper_horizontal_load * base_height
                
                # 截面抵抗矩 = (长 × 宽²)/6 (m³)，宽取底板较长边尺寸
                longer_side = max(base_length, base_bottom_width)
                shorter_side = min(base_length, base_bottom_width)
                section_modulus = (shorter_side * longer_side ** 2) / 6
                
                # 计算Pkmax和Pkmin
                pkmax = (total_load / base_area) + (base_moment / section_modulus)
                pkmin = (total_load / base_area) - (base_moment / section_modulus)
            else:
                # 当水平荷载为0时，Pkmax和Pkmin等于基底压力
                pkmax = base_pressure
                pkmin = base_pressure
        else:
            # 梯形基础不计算 Pkmax 和 Pkmin
            pkmax = 0
            pkmin = 0
        
        # 验算地基承载力
        is_satisfied = base_pressure <= bearing_capacity
        
        return is_satisfied, basic_weight, soil_load, total_load, base_pressure, self.CONCRETE_DENSITY, pkmax, pkmin, base_moment, section_modulus

    def check_overturning(self, upper_vertical_load, upper_horizontal_load, base_length, base_bottom_width, base_height, foundation_style, base_column_length=0, base_column_width=0, base_plate_height=0, base_top_width=0):
        """验算管墩抗倾覆是否满足要求

        Args:
            upper_vertical_load: 上部垂直荷载 (KN)
            upper_horizontal_load: 上部水平荷载 (KN)
            base_length: 底板长度 (m)
            base_bottom_width: 底板宽度 (m)
            base_height: 基础高度 (m)
            foundation_style: 基础样式 ("T型基础" 或 "梯形基础")
            base_column_length: 基础短柱长度 (m)，仅T型基础使用
            base_column_width: 基础短柱宽度 (m)，仅T型基础使用
            base_plate_height: 底板高度 (m)，仅T型基础使用
            base_top_width: 基础顶面宽度 (m)，仅梯形基础使用

        Returns:
            tuple: (是否满足要求, 抗倾覆力矩, 倾覆力矩, 抗倾覆安全系数, 总垂直荷载, 力臂长度)
        """
        # 计算基础自重 (KN)
        # 使用 calculate_basic_volume 函数计算基础体积
        basic_volume = self.calculate_basic_volume(
            base_length, base_bottom_width, base_top_width, base_height, 
            0, 0, 0, foundation_style
        )
        
        basic_weight = basic_volume * self.CONCRETE_DENSITY
        
        # 计算总垂直荷载 (KN)
        total_vertical_load = upper_vertical_load + basic_weight
        
        # 计算倾覆力矩和抗倾覆力矩
        # 假设水平荷载作用点高度为基础高度
        horizontal_load_height = base_height
        
        # 倾覆力矩 = 水平荷载 × 作用高度
        overturning_moment = upper_horizontal_load * horizontal_load_height
        
        # 抗倾覆力矩 = 总垂直荷载 × 基础底面形心到倾覆点的距离
        # 假设倾覆点为基础底面的边缘，取基础宽度的一半作为力臂
        # 这里取基础底面的最小尺寸作为计算宽度
        foundation_width = min(base_length, base_bottom_width)
        arm_length = foundation_width / 2
        
        # 抗倾覆力矩
        resisting_moment = total_vertical_load * arm_length
        
        # 计算抗倾覆安全系数
        if overturning_moment > 0:
            safety_factor = resisting_moment / overturning_moment
        else:
            # 当没有水平荷载时，安全系数为无穷大
            safety_factor = float('inf')
        
        # 抗倾覆安全系数一般要求大于1.6
        is_satisfied = safety_factor >= 1.6
        
        return is_satisfied, resisting_moment, overturning_moment, safety_factor, total_vertical_load, arm_length