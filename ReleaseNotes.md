# Release Notes

## 2026.03.27-preview

### 本次预览版说明
- 预览版打包完成：`dist/FugoToolbox.exe`
- 打包方式：`PyInstaller --clean FugoToolbox.spec`
- 生成时间：2026-03-27 08:42（本地时间）

### 主要修改内容

#### 1) 型钢特性表（Steel_Shape_Table）
- 修复“不等边角钢（2016）”部分字段显示为 0 的问题。
- 修复点包括：
  - `table_config.py` 中类型匹配顺序调整：先匹配“不等边角钢”，避免被“等边角钢”子串误匹配。
  - `database.py` 中不等边角钢数据映射修正：
    - 新增 `X0`、`Y0` 重心距离字段映射；
    - 惯性半径字段由错误的 `iy/iu` 映射调整为 `ry/ru` 对应输出字段。
  - `models.py` 中补充模型字段：新增 `X0`、`Y0`，并加入 `to_dict/from_dict` 序列化映射。

#### 2) YJK_Column_Force
- 在界面新增“使用说明”按钮。
- 新增使用说明弹窗（QDialog + QTextEdit），覆盖：
  - 原版/探索者两种模式使用流程；
  - 压力、拉力、全部导出规则；
  - Excel/TXT 导出格式说明；
  - 常见问题与排查提示。

#### 3) Basic_Block
- 本次预览版中未检测到 `plugins/Basic_Block` 目录下代码差异（无新增修改提交）。
- 仍建议按下方“验证建议”进行回归验证，确保插件行为正常。

### 已知说明
- `dist` 目录中保留了历史产物：
  - `符构工具箱v1.0.exe`
  - `FUGUToolsv1.0.exe.zip`
- 本次预览版请以最新生成的 `FugoToolbox.exe` 为准。

### 验证建议
- 启动应用后，重点检查各插件页面能否正常打开。
- 特别验证：`型钢特性表`、`YJK_Column_Force`、`Basic_Block`。
