import json
import sys

from pypdf import PdfReader, PdfWriter

from extract_form_field_info import get_field_info


# 填充 PDF 中的可填写表单字段。详见 forms.md。


def fill_pdf_fields(input_pdf_path: str, fields_json_path: str, output_pdf_path: str):
    """根据字段值 JSON 填充 PDF 可填写表单字段"""
    with open(fields_json_path) as f:
        fields = json.load(f)
    # 按页码分组字段。
    fields_by_page = {}
    for field in fields:
        if "value" in field:
            field_id = field["field_id"]
            page = field["page"]
            if page not in fields_by_page:
                fields_by_page[page] = {}
            fields_by_page[page][field_id] = field["value"]  # 按页码和字段 ID 组织字段值
    
    reader = PdfReader(input_pdf_path)

    has_error = False
    field_info = get_field_info(reader)  # 获取 PDF 中的字段信息
    fields_by_ids = {f["field_id"]: f for f in field_info}  # 创建字段 ID 到字段信息的映射
    for field in fields:
        existing_field = fields_by_ids.get(field["field_id"])
        if not existing_field:
            has_error = True
            print(f"ERROR: `{field['field_id']}` 不是有效的字段 ID")
        elif field["page"] != existing_field["page"]:
            has_error = True
            print(f"ERROR: 字段 `{field['field_id']}` 的页码不正确 (收到 {field['page']}，预期 {existing_field['page']})")
        else:
            if "value" in field:
                err = validation_error_for_field_value(existing_field, field["value"])
                if err:
                    print(err)
                    has_error = True
    if has_error:
        sys.exit(1)

    writer = PdfWriter(clone_from=reader)
    for page, field_values in fields_by_page.items():
        # 更新指定页面的表单字段值
        writer.update_page_form_field_values(writer.pages[page - 1], field_values, auto_regenerate=False)

    # 这似乎是许多 PDF 阅读器正确格式化表单值所必需的。
    # 即使用户未进行任何更改，这也可能导致阅读器显示"保存更改"对话框。
    writer.set_need_appearances_writer(True)
    
    with open(output_pdf_path, "wb") as f:
        writer.write(f)


def validation_error_for_field_value(field_info, field_value):
    """验证字段值是否有效，返回错误消息或 None"""
    field_type = field_info["type"]
    field_id = field_info["field_id"]
    if field_type == "checkbox":
        checked_val = field_info["checked_value"]
        unchecked_val = field_info["unchecked_value"]
        if field_value != checked_val and field_value != unchecked_val:
            return f'ERROR: 复选框字段 "{field_id}" 的值 "{field_value}" 无效。选中值为 "{checked_val}"，未选中值为 "{unchecked_val}"'
    elif field_type == "radio_group":
        option_values = [opt["value"] for opt in field_info["radio_options"]]
        if field_value not in option_values:
            return f'ERROR: 单选组字段 "{field_id}" 的值 "{field_value}" 无效。有效值为: {option_values}' 
    elif field_type == "choice":
        choice_values = [opt["value"] for opt in field_info["choice_options"]]
        if field_value not in choice_values:
            return f'ERROR: 多选字段 "{field_id}" 的值 "{field_value}" 无效。有效值为: {choice_values}'
    return None


# pypdf（至少 5.7.0 版本）在设置选择列表字段的值时存在一个 bug。
# 在 _writer.py 约第 966 行：
#
# if field.get(FA.FT, "/Tx") == "/Ch" and field_flags & FA.FfBits.Combo == 0:
#     txt = "\n".join(annotation.get_inherited(FA.Opt, []))
#
# 问题是对于选择列表，`get_inherited` 返回的是二维列表，如
# [["value1", "Text 1"], ["value2", "Text 2"], ...]
# 这导致 `join` 抛出 TypeError，因为它期望的是字符串可迭代对象。
# 这个糟糕的解决方案是修补 `get_inherited` 以返回值字符串的列表。
# 我们调用原始方法，仅当 `get_inherited` 的参数是 `FA.Opt`
# 且返回值是二维列表时调整返回值。
def monkeypatch_pydpf_method():
    """修补 pypdf 的 get_inherited 方法以处理选择列表字段"""
    from pypdf.generic import DictionaryObject
    from pypdf.constants import FieldDictionaryAttributes

    original_get_inherited = DictionaryObject.get_inherited  # 保存原始方法引用

    def patched_get_inherited(self, key: str, default = None):
        """修补后的 get_inherited 方法，对选择列表字段特殊处理"""
        result = original_get_inherited(self, key, default)
        if key == FieldDictionaryAttributes.Opt:
            # 如果是选择列表选项字段，将二维列表转换为一维值列表
            if isinstance(result, list) and all(isinstance(v, list) and len(v) == 2 for v in result):
                result = [r[0] for r in result]
        return result

    DictionaryObject.get_inherited = patched_get_inherited  # 应用修补


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: fill_fillable_fields.py [输入 PDF] [字段值.json] [输出 PDF]")
        sys.exit(1)
    monkeypatch_pydpf_method()  # 应用 pypdf 兼容性修补
    input_pdf = sys.argv[1]
    fields_json = sys.argv[2]
    output_pdf = sys.argv[3]
    fill_pdf_fields(input_pdf, fields_json, output_pdf)
