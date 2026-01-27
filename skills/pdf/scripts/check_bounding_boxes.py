from dataclasses import dataclass
import json
import sys


# 大型语言模型 创建的用于分析 PDF 的 `fields.json` 文件的检查脚本
# 确保文件中的边界框没有重叠。详见 forms.md。


@dataclass
class RectAndField:
    rect: list[float]       # 边界框坐标 [左, 上, 右, 下]
    rect_type: str          # 边界框类型: "label" 或 "entry"
    field: dict             # 关联的字段数据


# 返回一条消息列表，打印到 stdout 供 大型语言模型 读取。
def get_bounding_box_messages(fields_json_stream) -> list[str]:
    messages = []
    fields = json.load(fields_json_stream)
    messages.append(f"读取了 {len(fields['form_fields'])} 个字段")

    def rects_intersect(r1, r2):
        """检查两个边界框是否相交"""
        disjoint_horizontal = r1[0] >= r2[2] or r1[2] <= r2[0]  # 水平方向不相交
        disjoint_vertical = r1[1] >= r2[3] or r1[3] <= r2[1]    # 垂直方向不相交
        return not (disjoint_horizontal or disjoint_vertical)  # 任一方向相交即为相交

    rects_and_fields = []
    for f in fields["form_fields"]:
        # 为每个字段收集标签和输入边界框
        rects_and_fields.append(RectAndField(f["label_bounding_box"], "label", f))
        rects_and_fields.append(RectAndField(f["entry_bounding_box"], "entry", f))

    has_error = False
    for i, ri in enumerate(rects_and_fields):
        # 这是 O(N^2) 的复杂度；如果成为问题可以优化。
        for j in range(i + 1, len(rects_and_fields)):
            rj = rects_and_fields[j]
            # 只检查同一页面上的边界框是否相交
            if ri.field["page_number"] == rj.field["page_number"] and rects_intersect(ri.rect, rj.rect):
                has_error = True
                if ri.field is rj.field:
                    # 同一字段的标签和输入框相交
                    messages.append(f"FAILURE: 字段 `{ri.field['description']}` 的标签和输入边界框相交 ({ri.rect}, {rj.rect})")
                else:
                    # 不同字段的边界框相交
                    messages.append(f"FAILURE: 字段 `{ri.field['description']}` 的 {ri.rect_type} 边界框 ({ri.rect}) 与字段 `{rj.field['description']}` 的 {rj.rect_type} 边界框 ({rj.rect}) 相交")
                if len(messages) >= 20:
                    messages.append("中止进一步检查；请修复边界框后重试")
                    return messages
        if ri.rect_type == "entry":
            # 检查输入框高度是否足够容纳文本
            if "entry_text" in ri.field:
                font_size = ri.field["entry_text"].get("font_size", 14)  # 默认字体大小为 14
                entry_height = ri.rect[3] - ri.rect[1]  # 计算输入框高度
                if entry_height < font_size:
                    has_error = True
                    messages.append(f"FAILURE: 字段 `{ri.field['description']}` 的输入边界框高度 ({entry_height}) 对于文本内容太短 (字体大小: {font_size})。请增加框的高度或减小字体大小。")
                    if len(messages) >= 20:
                        messages.append("中止进一步检查；请修复边界框后重试")
                        return messages

    if not has_error:
        messages.append("SUCCESS: 所有边界框都有效")
    return messages

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: check_bounding_boxes.py [fields.json]")
        sys.exit(1)
    # 输入文件应为 forms.md 中描述的 `fields.json` 格式。
    with open(sys.argv[1]) as f:
        messages = get_bounding_box_messages(f)
    for msg in messages:
        print(msg)
