"""水池基础材料用量计算与抗浮验算逻辑模块。

本模块实现以下能力：
1. 按给定几何参数计算底板、池壁、顶板、柱、隔墙、平衡层、换填等体积；
2. 计算多工况（空载/满水/实际水深）抗浮稳定安全系数；
3. 给出不满足工况时的定量补强建议。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PoolFoundationInput:
    """水池基础计算输入参数。"""

    # -----------------------
    # 一、几何参数
    # -----------------------
    L: float  # 水池内长 (m)
    W: float  # 水池内宽 (m)
    H_total: float  # 水池总高（底板顶到顶板顶）(m)
    H_out: float  # 高出地面高度 (m) —— 本模块暂不参与核心计算，保留扩展
    h_slab: float  # 顶板厚度 (m)
    t_wall: float  # 池壁厚度 (m)
    h_footing: float  # 底板厚度 (m)
    b_overhang: float  # 底板外挑宽度 (m)

    # -----------------------
    # 二、平衡层与换填参数
    # -----------------------
    has_balancing_layer: bool  # 是否有平衡层（决定抗浮受力面积分支）
    c_bal_overhang: float  # 平衡层宽出底板距离 (m)
    h_bal: float  # 平衡层厚度 (m)
    gamma_bal: float = 18.0  # 平衡层重度 (kN/m³)
    h_cushion: float = 0.0  # 换填厚度 (m)
    d_cushion_overhang: float = 0.0  # 换填宽出平衡层/底板距离 (m)
    gamma_cushion: float = 19.0  # 换填重度 (kN/m³)
    h_mat: float = 0.0  # 垫层厚度 (m)

    # -----------------------
    # 三、内部构件参数
    # -----------------------
    V_partition_total: float = 0.0  # 隔墙混凝土总量 (m³)
    column_a: float = 0.0  # 柱截面长 (m)
    column_b: float = 0.0  # 柱截面宽 (m)
    column_height_type: str = "内净高"  # “内净高” 或 “自定义”
    column_height_custom: float = 0.0  # 自定义柱高 (m)
    column_count: int = 0  # 柱数量

    # -----------------------
    # 四、抗浮参数
    # -----------------------
    water_table_elev: float = 0.0  # 地下水位标高 (m)
    bottom_elev: float = 0.0  # 底板底标高 (m)
    gamma_water: float = 10.0  # 水重度 (kN/m³)
    gamma_concrete: float = 25.0  # 混凝土重度 (kN/m³)
    water_depth_inner: float = 0.0  # 池内实际水深 (m)
    gamma_soil_natural: float = 18.0  # 外挑填土天然重度 (kN/m³)
    gamma_soil_sat: float = 18.0  # 外挑填土饱和重度 (kN/m³)


class PoolTankFoundationLogic:
    """水池基础材料与抗浮验算计算器。"""

    def _validate_input(self, p: PoolFoundationInput):
        """输入校验。

        说明：
        - 只校验物理上必须合理的参数；
        - H_out 当前为扩展预留参数，不参与本次约束。
        """
        non_negative_fields = {
            "L": p.L,
            "W": p.W,
            "H_total": p.H_total,
            "h_slab": p.h_slab,
            "t_wall": p.t_wall,
            "h_footing": p.h_footing,
            "b_overhang": p.b_overhang,
            "c_bal_overhang": p.c_bal_overhang,
            "h_bal": p.h_bal,
            "gamma_bal": p.gamma_bal,
            "h_cushion": p.h_cushion,
            "d_cushion_overhang": p.d_cushion_overhang,
            "gamma_cushion": p.gamma_cushion,
            "V_partition_total": p.V_partition_total,
            "column_a": p.column_a,
            "column_b": p.column_b,
            "column_height_custom": p.column_height_custom,
            "column_count": p.column_count,
            "gamma_water": p.gamma_water,
            "gamma_concrete": p.gamma_concrete,
            "water_depth_inner": p.water_depth_inner,
        }
        for field_name, value in non_negative_fields.items():
            if value < 0:
                raise ValueError(f"参数 {field_name} 不能为负值")

        if p.L <= 0 or p.W <= 0:
            raise ValueError("内长 L 和内宽 W 必须大于0")

        if p.H_total <= 0:
            raise ValueError("总高 H_total 必须大于0")

        if p.h_slab >= p.H_total:
            raise ValueError("顶板厚度 h_slab 必须小于总高 H_total，否则内净高<=0")

        if p.column_height_type not in ("内净高", "自定义"):
            raise ValueError("column_height_type 仅允许“内净高”或“自定义”")

        if p.column_height_type == "自定义" and p.column_count > 0 and p.column_height_custom <= 0:
            raise ValueError("选择自定义柱高时，column_height_custom 必须大于0")

        # 若无平衡层，则相关几何按0处理，防止误输入带来歧义。
        if not p.has_balancing_layer and (p.c_bal_overhang != 0 or p.h_bal != 0):
            # 不强制报错，允许输入界面保留历史值，逻辑里自动忽略。
            pass

    @staticmethod
    def _safe_divide(numerator: float, denominator: float) -> float:
        """安全除法：浮力为0时返回正无穷，表示不存在上浮驱动力。"""
        if denominator <= 0:
            return float("inf")
        return numerator / denominator

    def calculate(self, p: PoolFoundationInput) -> Dict:
        """执行完整计算并返回结果字典。"""
        self._validate_input(p)

        # ==================================================
        # 1) 几何尺寸与材料用量计算
        # ==================================================
        # 内部净高：用于池内水容积与默认柱高
        H_in = p.H_total - p.h_slab

        # 底板
        L_base = p.L + 2 * p.t_wall + 2 * p.b_overhang
        W_base = p.W + 2 * p.t_wall + 2 * p.b_overhang
        V_base = L_base * W_base * p.h_footing

        # 平衡层分支
        if p.has_balancing_layer:
            L_bal = L_base + 2 * p.c_bal_overhang
            W_bal = W_base + 2 * p.c_bal_overhang
            V_bal = L_bal * W_bal * p.h_bal
        else:
            # 按要求：无平衡层时，后续换填几何基准取底板尺寸
            L_bal = L_base
            W_bal = W_base
            V_bal = 0.0

        # 换填砂石
        # 有平衡层：换填基准为平衡层尺寸 + 宽出距离
        # 无平衡层：换填基准为底板尺寸 + 固定0.1m（两侧共+0.2m）+ 宽出距离
        if p.has_balancing_layer:
            L_cushion = L_bal + 2 * p.d_cushion_overhang
            W_cushion = W_bal + 2 * p.d_cushion_overhang
        else:
            L_cushion = L_base + 0.2 + 2 * p.d_cushion_overhang
            W_cushion = W_base + 0.2 + 2 * p.d_cushion_overhang
        V_cushion = L_cushion * W_cushion * p.h_cushion

        # 垫层（固定基准：底板尺寸 + 两侧各0.1m，即+0.2m）
        L_mat = L_base + 0.2
        W_mat = W_base + 0.2
        V_mat = L_mat * W_mat * p.h_mat

        # 池壁（按用户修订：池壁总高度=水池高度-顶板厚度）
        H_wall_total = p.H_total - p.h_slab
        # 池壁中心线总长（按用户修订）
        # = 2×(内长+池壁厚度) + 2×(内宽+池壁厚度)
        L_wall_centerline = (p.L + p.t_wall) * 2 + (p.W + p.t_wall) * 2
        V_wall = L_wall_centerline * p.t_wall * H_wall_total

        # 顶板（按用户修订：不含底板外挑，仅按池内净尺寸+两侧池壁厚度计算）
        L_roof = p.L + 2 * p.t_wall
        W_roof = p.W + 2 * p.t_wall
        V_roof = L_roof * W_roof * p.h_slab

        # 柱
        if p.column_height_type == "内净高":
            H_column = H_in
        else:
            H_column = p.column_height_custom

        V_column_single = p.column_a * p.column_b * H_column if p.column_count > 0 else 0.0
        V_columns = p.column_count * V_column_single

        # 汇总混凝土体积
        V_concrete_total = V_base + V_wall + V_roof + p.V_partition_total + V_columns

        # ==================================================
        # 2) 抗浮验算
        # ==================================================
        # A) 抗浮受力面积
        A_buoy = L_bal * W_bal if p.has_balancing_layer else L_base * W_base

        # B) 浮力
        # 有平衡层时，浮力受力底面为平衡层底面（底板底再往下 h_bal）
        buoy_base_elev = p.bottom_elev - p.h_bal if p.has_balancing_layer else p.bottom_elev
        H_water_height = max(0.0, p.water_table_elev - buoy_base_elev)
        F_buoy = A_buoy * p.gamma_water * H_water_height

        # C) 抗浮总重量（不含池内水）
        # 按用户最新要求：换填重量不参与抗浮总重量计算，仅作为材料统计量输出。
        G_self = V_concrete_total * p.gamma_concrete
        G_bal = V_bal * p.gamma_bal

        # 填土有效重度 = 饱和重度 - 水重度
        gamma_soil_eff = p.gamma_soil_sat - p.gamma_water

        # ---- 1) 底板外挑部分填土重量（从底板顶面起算）----
        # 外挑环形面积 = 底板总面积 - (底板长-2×外挑) × (底板宽-2×外挑)
        L_inner_wall = L_base - 2 * p.b_overhang  # = L + 2*t_wall
        W_inner_wall = W_base - 2 * p.b_overhang  # = W + 2*t_wall
        A_overhang_soil = L_base * W_base - L_inner_wall * W_inner_wall
        # 底板顶标高 = bottom_elev + h_footing
        footing_top_elev = p.bottom_elev + p.h_footing
        # 外挑区填土总高度（底板顶面到地面0标高）
        H_overhang_soil_total = max(0.0, 0.0 - footing_top_elev)
        if H_overhang_soil_total > 0 and p.b_overhang > 0:
            # 水位以下填土高度（底板顶到水位）
            H_overhang_below_wt = max(0.0, min(p.water_table_elev, 0.0) - footing_top_elev)
            # 水位以上填土高度
            H_overhang_above_wt = max(0.0, H_overhang_soil_total - H_overhang_below_wt)
            G_soil_overhang = A_overhang_soil * (
                H_overhang_above_wt * p.gamma_soil_natural
                + H_overhang_below_wt * gamma_soil_eff
            )
        else:
            H_overhang_below_wt = 0.0
            H_overhang_above_wt = 0.0
            G_soil_overhang = 0.0

        # ---- 2) 平衡层超出底板环形区填土重量（从底板底面起算）----
        if p.has_balancing_layer and p.c_bal_overhang > 0:
            A_bal_soil = L_bal * W_bal - L_base * W_base
            # 填土总高度（底板底面到地面0标高）
            H_bal_soil_total = max(0.0, 0.0 - p.bottom_elev)
            if H_bal_soil_total > 0:
                # 水位以下高度（底板底到水位）
                H_bal_below_wt = max(0.0, min(p.water_table_elev, 0.0) - p.bottom_elev)
                # 水位以上高度
                H_bal_above_wt = max(0.0, H_bal_soil_total - H_bal_below_wt)
                G_soil_bal = A_bal_soil * (
                    H_bal_above_wt * p.gamma_soil_natural
                    + H_bal_below_wt * gamma_soil_eff
                )
            else:
                H_bal_below_wt = 0.0
                H_bal_above_wt = 0.0
                G_soil_bal = 0.0
        else:
            A_bal_soil = 0.0
            H_bal_below_wt = 0.0
            H_bal_above_wt = 0.0
            G_soil_bal = 0.0

        G_total = G_self + G_bal + G_soil_overhang + G_soil_bal

        # D) 池内水重量
        V_water_max = p.L * p.W * H_in
        G_water_full = V_water_max * p.gamma_water

        h_water_actual = min(max(p.water_depth_inner, 0.0), H_in)
        G_water_actual = p.L * p.W * h_water_actual * p.gamma_water

        # E) 多工况安全系数
        K_full = self._safe_divide(G_total + G_water_full, F_buoy)
        K_actual = self._safe_divide(G_total + G_water_actual, F_buoy)
        K_empty = self._safe_divide(G_total, F_buoy)

        req_full = 1.05
        req_actual = 1.05
        req_empty = 1.10

        pass_full = K_full >= req_full
        pass_actual = K_actual >= req_actual
        pass_empty = K_empty >= req_empty

        # 综合判定：按常规控制空载和满水；实际水深工况单独给出。
        pass_overall = pass_full and pass_empty

        # ==================================================
        # 3) 不满足建议（定量+定性）
        # ==================================================
        suggestions: List[str] = []

        if F_buoy <= 0:
            suggestions.append("地下水位未高于底板底标高，当前浮力为0，抗浮天然满足。")
        else:
            # 以最不利系数要求换算“尚缺重量”
            deficit_empty = max(0.0, req_empty * F_buoy - G_total)
            deficit_full = max(0.0, req_full * F_buoy - (G_total + G_water_full))
            deficit_actual = max(0.0, req_actual * F_buoy - (G_total + G_water_actual))

            if deficit_empty > 0:
                suggestions.append(
                    f"空载工况尚缺抗浮重量约 {deficit_empty:.2f} kN。可优先增大底板外挑宽度、增加底板厚度，"
                    "或设置/加厚平衡层。"
                )

            if deficit_full > 0:
                suggestions.append(
                    f"满水工况尚缺抗浮重量约 {deficit_full:.2f} kN。可增大结构自重（如底板厚度、池壁厚度）或增强平衡层参数。"
                )

            if deficit_actual > 0:
                suggestions.append(
                    f"实际水深工况尚缺抗浮重量约 {deficit_actual:.2f} kN。可提高运行水深、增加配重或优化基础尺寸。"
                )

            if not p.has_balancing_layer and (not pass_empty or not pass_full or not pass_actual):
                suggestions.append("当前未设置平衡层，建议考虑增设平衡层，并适当加大平衡层外扩宽度与平衡层厚度。")

        return {
            "inputs": {
                "has_balancing_layer": p.has_balancing_layer,
                "column_height_type": p.column_height_type,
            },
            "geometry": {
                "H_in": H_in,
                "L_base": L_base,
                "W_base": W_base,
                "L_roof": L_roof,
                "W_roof": W_roof,
                "L_bal": L_bal,
                "W_bal": W_bal,
                "L_cushion": L_cushion,
                "W_cushion": W_cushion,
                "H_wall_total": H_wall_total,
                "L_wall_centerline": L_wall_centerline,
                "H_column": H_column,
                "A_buoy": A_buoy,
                "H_water_height": H_water_height,
                "h_water_actual": h_water_actual,
            },
            "volumes": {
                "V_base": V_base,
                "V_bal": V_bal,
                "V_cushion": V_cushion,
                "V_mat": V_mat,
                "V_wall": V_wall,
                "V_roof": V_roof,
                "V_column_single": V_column_single,
                "V_columns": V_columns,
                "V_partition_total": p.V_partition_total,
                "V_concrete_total": V_concrete_total,
                "V_water_max": V_water_max,
            },
            "weights": {
                "F_buoy": F_buoy,
                "G_self": G_self,
                "G_bal": G_bal,
                "gamma_soil_eff": gamma_soil_eff,
                "G_soil_overhang": G_soil_overhang,
                "A_overhang_soil": A_overhang_soil,
                "H_overhang_above_wt": H_overhang_above_wt,
                "H_overhang_below_wt": H_overhang_below_wt,
                "G_soil_bal": G_soil_bal,
                "A_bal_soil": A_bal_soil,
                "H_bal_above_wt": H_bal_above_wt,
                "H_bal_below_wt": H_bal_below_wt,
                "G_total": G_total,
                "G_water_full": G_water_full,
                "G_water_actual": G_water_actual,
            },
            "checks": {
                "K_full": K_full,
                "K_actual": K_actual,
                "K_empty": K_empty,
                "req_full": req_full,
                "req_actual": req_actual,
                "req_empty": req_empty,
                "pass_full": pass_full,
                "pass_actual": pass_actual,
                "pass_empty": pass_empty,
                "pass_overall": pass_overall,
            },
            "suggestions": suggestions,
        }
