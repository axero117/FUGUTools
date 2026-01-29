# 定义不同表类型的列配置
# 列配置格式: (数据字段名, 中文标题, 格式)
# 格式说明: 's' 表示字符串, '.1f' 表示浮点数保留1位小数, '.2f' 表示浮点数保留2位小数

TABLE_COLUMN_CONFIGS = {
    # H型钢2017系列
    'h_sections_2017': [
        ('model', '型号', 's'),
        ('height', '高度H\n(mm)', '.0f'),
        ('width', '宽度B\n(mm)', '.0f'),
        ('web_thickness', '腹板厚度t1\n(mm)', '.2f'),
        ('flange_thickness', '翼缘厚度t2\n(mm)', '.2f'),
        ('fillet_radius', '圆角半径r\n(mm)', '.2f'),
        ('area', '截面面积\n(cm²)', '.2f'),
        ('weight', '理论重量\n(kg/m)', '.2f'),
        ('surface_area', '表面积\n(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix\n(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy\n(cm⁴)', '.1f'),
        ('ix', '惯性半径ix\n(cm)', '.2f'),
        ('iy', '惯性半径iy\n(cm)', '.2f'),
        ('Wx', '截面模量Wx\n(cm³)', '.1f'),
        ('Wy', '截面模量Wy\n(cm³)', '.1f'),
    ],
    # H型钢2024
    'h_sections_2024': [
        ('model', '型号', 's'),
        ('height', '高度H\n(mm)', '.0f'),
        ('width', '宽度B\n(mm)', '.0f'),
        ('web_thickness', '腹板厚度t1\n(mm)', '.2f'),
        ('flange_thickness', '翼缘厚度t2\n(mm)', '.2f'),
        ('fillet_radius', '圆角半径r\n(mm)', '.2f'),
        ('area', '截面面积\n(cm²)', '.2f'),
        ('weight', '理论重量\n(kg/m)', '.2f'),
        ('surface_area', '表面积\n(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix\n(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy\n(cm⁴)', '.1f'),
        ('ix', '惯性半径ix\n(cm)', '.2f'),
        ('iy', '惯性半径iy\n(cm)', '.2f'),
        ('Wx', '截面模量Wx\n(cm³)', '.1f'),
        ('Wy', '截面模量Wy\n(cm³)', '.1f'),
    ],
    # I型钢2016
    'i_sections_2016': [
        ('model', '型号', 's'),
        ('height', '高度H\n(mm)', '.0f'),
        ('width', '宽度B\n(mm)', '.0f'),
        ('web_thickness', '腹板厚度t1\n(mm)', '.2f'),
        ('flange_thickness', '翼缘厚度t2\n(mm)', '.2f'),
        ('inner_fillet_radius', '内圆角半径r\'\n(mm)', '.2f'),
        ('fillet_radius', '圆角半径r\n(mm)', '.2f'),
        ('area', '截面面积\n(cm²)', '.2f'),
        ('weight', '理论重量\n(kg/m)', '.2f'),
        ('surface_area', '表面积\n(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix\n(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy\n(cm⁴)', '.1f'),
        ('ix', '惯性半径ix\n(cm)', '.2f'),
        ('iy', '惯性半径iy\n(cm)', '.2f'),
        ('Wx', '截面模量Wx\n(cm³)', '.1f'),
        ('Wy', '截面模量Wy\n(cm³)', '.1f'),
    ],
    # 等边角钢2016
    'l_sections_2016': [
        ('model', '型号', 's'),
        ('side_width', '边宽B\n(mm)', '.1f'),
        ('edge_thickness', '边厚t\n(mm)', '.2f'),
        ('round_radius', '圆角半径r\n(mm)', '.2f'),
        ('area', '截面面积\n(cm²)', '.2f'),
        ('weight', '理论重量\n(kg/m)', '.2f'),
        ('surface_area', '表面积\n(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix\n(cm⁴)', '.1f'),
        ('Ix1', '惯性矩IX1\n(cm⁴)', '.1f'),
        ('Ix0', '惯性矩IX0\n(cm⁴)', '.1f'),
        ('Iy0', '惯性矩Iy0\n(cm⁴)', '.1f'),
        ('ix', '惯性半径ix\n(cm)', '.2f'),
        ('ix0', '惯性半径rx0\n(cm)', '.2f'),
        ('iy', '惯性半径iy0\n(cm)', '.2f'),
        ('Wx', '截面模量Wx\n(cm³)', '.1f'),
        ('Wx0', '截面模量WX0\n(cm³)', '.1f'),
        ('Wy0', '截面模量Wy0\n(cm³)', '.1f'),
        ('Z0', '重心距离Z0\n(cm)', '.2f'),
    ],
    # 不等边角钢2016
    'non_l_sections_2016': [
        ('model', '型号', 's'),
        ('long_side_width', '长边宽B\n(mm)', '.1f'),
        ('short_side_width', '短边宽b\n(mm)', '.1f'),
        ('edge_thickness', '边厚t\n(mm)', '.2f'),
        ('round_radius', '圆角半径r\n(mm)', '.2f'),
        ('X0', '重心距离X0\n(cm)', '.2f'),
        ('Y0', '重心距离Y0\n(cm)', '.2f'),
        ('area', '截面面积\n(cm²)', '.2f'),
        ('weight', '理论重量\n(kg/m)', '.2f'),
        ('surface_area', '表面积\n(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix\n(cm⁴)', '.1f'),
        ('Ix1', '惯性矩Ix1\n(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy\n(cm⁴)', '.1f'),
        ('Iy1', '惯性矩Iy1\n(cm⁴)', '.2f'),
        ('ix', '惯性半径ix\n(cm)', '.2f'),
        ('ry', '惯性半径iy\n(cm)', '.2f'),
        ('Wx', '截面模量Wx\n(cm³)', '.1f'),
        ('Wy', '截面模量Wy\n(cm³)', '.1f'),
        ('Iu', '惯性矩Iu\n(cm⁴)', '.1f'),
        ('ru', '惯性半径iu\n(cm)', '.2f'),
        ('Wu', '截面模量Wu\n(cm³)', '.1f'),
    ],
    # C型钢2016
    'c_sections_2016': [
        ('model', '型号', 's'),
        ('height', '高度H\n(mm)', '.1f'),
        ('width', '宽度B\n(mm)', '.1f'),
        ('flange_thickness', '厚度t\n(mm)', '.2f'),
        ('round_radius', '圆角半径r\n(mm)', '.2f'),
        ('area', '截面面积\n(cm²)', '.2f'),
        ('weight', '理论重量\n(kg/m)', '.2f'),
        ('surface_area', '表面积\n(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix\n(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy\n(cm⁴)', '.1f'),
        ('ix', '惯性半径ix\n(cm)', '.2f'),
        ('iy', '惯性半径iy\n(cm)', '.2f'),
        ('Wx', '截面模量Wx\n(cm³)', '.1f'),
        ('Wy', '截面模量Wy\n(cm³)', '.1f'),
    ],
}


def get_table_config(shape_type):
    """根据型钢类型获取表格列配置
    
    Args:
        shape_type: 型钢类型
        
    Returns:
        tuple: (列配置列表, 表名)
    """
    # 使用模糊匹配来识别型钢类型
    if 'H型钢' in shape_type and '2024' in shape_type:
        return TABLE_COLUMN_CONFIGS['h_sections_2024'], 'h_sections_2024'
    elif 'HW型钢' in shape_type and '2017' in shape_type:
        return TABLE_COLUMN_CONFIGS['h_sections_2017'], 'h_sections_2017'
    elif 'HM型钢' in shape_type and '2017' in shape_type:
        return TABLE_COLUMN_CONFIGS['h_sections_2017'], 'h_sections_2017'
    elif 'HN型钢' in shape_type and '2017' in shape_type:
        return TABLE_COLUMN_CONFIGS['h_sections_2017'], 'h_sections_2017'
    elif 'HT型钢' in shape_type and '2017' in shape_type:
        return TABLE_COLUMN_CONFIGS['h_sections_2017'], 'h_sections_2017'
    elif 'I型钢' in shape_type and '2016' in shape_type:
        return TABLE_COLUMN_CONFIGS['i_sections_2016'], 'i_sections_2016'
    elif '等边角钢' in shape_type and '2016' in shape_type:
        return TABLE_COLUMN_CONFIGS['l_sections_2016'], 'l_sections_2016'
    elif '不等边角钢' in shape_type and '2016' in shape_type:
        return TABLE_COLUMN_CONFIGS[
            'non_l_sections_2016'], 'non_l_sections_2016'
    elif 'C型钢' in shape_type and '2016' in shape_type:
        return TABLE_COLUMN_CONFIGS['c_sections_2016'], 'c_sections_2016'
    else:
        # 默认返回空配置
        return None, None
