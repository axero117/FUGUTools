# 定义不同表类型的列配置
# 列配置格式: (数据字段名, 中文标题, 格式)
# 格式说明: 's' 表示字符串, '.1f' 表示浮点数保留1位小数, '.2f' 表示浮点数保留2位小数

TABLE_COLUMN_CONFIGS = {
    # H型钢2017系列
    'h_sections_2017': [
        ('model', '型号', 's'),
        ('height', '高度H(mm)', '.1f'),
        ('width', '宽度B(mm)', '.1f'),
        ('web_thickness', '腹板厚度t1(mm)', '.2f'),
        ('flange_thickness', '翼缘厚度t2(mm)', '.2f'),
        ('fillet_radius', '圆角半径r(mm)', '.2f'),
        ('area', '截面面积(cm²)', '.2f'),
        ('weight', '理论重量(kg/m)', '.2f'),
        ('surface_area', '表面积(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy(cm⁴)', '.1f'),
        ('ix', '惯性半径ix(cm)', '.2f'),
        ('iy', '惯性半径iy(cm)', '.2f'),
        ('Wx', '截面模量Wx(cm³)', '.1f'),
        ('Wy', '截面模量Wy(cm³)', '.1f'),
    ],
    # H型钢2024
    'h_sections_2024': [
        ('model', '型号', 's'),
        ('height', '高度H(mm)', '.1f'),
        ('width', '宽度B(mm)', '.1f'),
        ('web_thickness', '腹板厚度t1(mm)', '.2f'),
        ('flange_thickness', '翼缘厚度t2(mm)', '.2f'),
        ('fillet_radius', '圆角半径r(mm)', '.2f'),
        ('area', '截面面积(cm²)', '.2f'),
        ('weight', '理论重量(kg/m)', '.2f'),
        ('surface_area', '表面积(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy(cm⁴)', '.1f'),
        ('ix', '惯性半径ix(cm)', '.2f'),
        ('iy', '惯性半径iy(cm)', '.2f'),
        ('Wx', '截面模量Wx(cm³)', '.1f'),
        ('Wy', '截面模量Wy(cm³)', '.1f'),
    ],
    # I型钢2016
    'i_sections_2016': [
        ('model', '型号', 's'),
        ('height', '高度H(mm)', '.1f'),
        ('width', '宽度B(mm)', '.1f'),
        ('web_thickness', '腹板厚度t1(mm)', '.2f'),
        ('flange_thickness', '翼缘厚度t2(mm)', '.2f'),
        ('inner_fillet_radius', '内圆角半径r\'(mm)', '.2f'),
        ('fillet_radius', '圆角半径r(mm)', '.2f'),
        ('area', '截面面积(cm²)', '.2f'),
        ('weight', '理论重量(kg/m)', '.2f'),
        ('surface_area', '表面积(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy(cm⁴)', '.1f'),
        ('ix', '惯性半径ix(cm)', '.2f'),
        ('iy', '惯性半径iy(cm)', '.2f'),
        ('Wx', '截面模量Wx(cm³)', '.1f'),
        ('Wy', '截面模量Wy(cm³)', '.1f'),
    ],
    # 等边角钢2016
    'l_sections_2016': [
        ('section_name', '型号', 's'),
        ('side_width', '边宽B(mm)', '.1f'),
        ('edge_thickness', '边厚t(mm)', '.2f'),
        ('round_radius', '圆角半径r(mm)', '.2f'),
        ('area', '截面面积(cm²)', '.2f'),
        ('weight', '理论重量(kg/m)', '.2f'),
        ('surface_area', '表面积(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix(cm⁴)', '.1f'),
        ('IX1', '惯性矩IX1(cm⁴)', '.1f'),
        ('IX0', '惯性矩IX0(cm⁴)', '.1f'),
        ('Iy0', '惯性矩Iy0(cm⁴)', '.1f'),
        ('ix', '惯性半径ix(cm)', '.2f'),
        ('ix0', '惯性半径rx0(cm)', '.2f'),
        ('iy0', '惯性半径iy0(cm)', '.2f'),
        ('Wx', '截面模量Wx(cm³)', '.1f'),
        ('WX0', '截面模量WX0(cm³)', '.1f'),
        ('Wy0', '截面模量Wy0(cm³)', '.1f'),
        ('Z0', '重心距离Z0(cm)', '.2f'),
    ],
    # 不等边角钢2016
    'non_l_sections_2016': [
        ('section_name', '型号', 's'),
        ('long_side_width', '长边宽B(mm)', '.1f'),
        ('short_side_width', '短边宽b(mm)', '.1f'),
        ('edge_thickness', '边厚t(mm)', '.2f'),
        ('round_radius', '圆角半径r(mm)', '.2f'),
        ('X0', '重心距离X0(cm)', '.2f'),
        ('Y0', '重心距离Y0(cm)', '.2f'),
        ('area', '截面面积(cm²)', '.2f'),
        ('weight', '理论重量(kg/m)', '.2f'),
        ('surface_area', '表面积(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix(cm⁴)', '.1f'),
        ('Ix1', '惯性矩Ix1(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy(cm⁴)', '.1f'),
        ('Iy1', '惯性矩Iy1(cm⁴)', '.2f'),
        ('rx', '惯性半径ix(cm)', '.2f'),
        ('ry', '惯性半径iy(cm)', '.2f'),
        ('Wx', '截面模量Wx(cm³)', '.1f'),
        ('Wy', '截面模量Wy(cm³)', '.1f'),
        ('Iu', '惯性矩Iu(cm⁴)', '.1f'),
        ('ru', '惯性半径iu(cm)', '.2f'),
        ('Wu', '截面模量Wu(cm³)', '.1f'),
    ],
    # C型钢2016
    'c_sections_2016': [
        ('model', '型号', 's'),
        ('height', '高度H(mm)', '.1f'),
        ('width', '宽度B(mm)', '.1f'),
        ('flange_thickness', '厚度t(mm)', '.2f'),
        ('fillet_radius', '圆角半径r(mm)', '.2f'),
        ('area', '截面面积(cm²)', '.2f'),
        ('weight', '理论重量(kg/m)', '.2f'),
        ('surface_area', '表面积(m²/m)', '.3f'),
        ('Ix', '惯性矩Ix(cm⁴)', '.1f'),
        ('Iy', '惯性矩Iy(cm⁴)', '.1f'),
        ('ix', '惯性半径ix(cm)', '.2f'),
        ('iy', '惯性半径iy(cm)', '.2f'),
        ('Wx', '截面模量Wx(cm³)', '.1f'),
        ('Wy', '截面模量Wy(cm³)', '.1f'),
    ],
}

def get_table_config(shape_type):
    """根据型钢类型获取表格列配置
    
    Args:
        shape_type: 型钢类型
        
    Returns:
        tuple: (列配置列表, 表名)
    """
    if shape_type.endswith('型钢截面表（2017）'):
        return TABLE_COLUMN_CONFIGS['h_sections_2017'], 'h_sections_2017'
    elif shape_type == 'H型钢截面表（2024）':
        return TABLE_COLUMN_CONFIGS['h_sections_2024'], 'h_sections_2024'
    elif shape_type == 'I型钢截面表（2016）':
        return TABLE_COLUMN_CONFIGS['i_sections_2016'], 'i_sections_2016'
    elif shape_type == '等边角钢截面表（2016）':
        return TABLE_COLUMN_CONFIGS['l_sections_2016'], 'l_sections_2016'
    elif shape_type == '不等边角钢截面表（2016）':
        return TABLE_COLUMN_CONFIGS['non_l_sections_2016'], 'non_l_sections_2016'
    elif shape_type == 'C型钢截面表（2016）':
        return TABLE_COLUMN_CONFIGS['c_sections_2016'], 'c_sections_2016'
    else:
        return None, None