import json
import sys

from PIL import Image, ImageDraw


# 创建"验证"图像，为 大型语言模型 在确定 PDF 中文本注释添加位置时创建的边界框信息绘制矩形框。
# 详见 forms.md。


def create_validation_image(page_number, fields_json_path, input_path, output_path):
    """根据 fields.json 中的边界框信息创建验证图像，在输入图像上绘制红蓝矩形框"""
    # 输入文件应为 forms.md 中描述的 `fields.json` 格式。
    with open(fields_json_path, 'r') as f:
        data = json.load(f)

        img = Image.open(input_path)  # 打开输入图像
        draw = ImageDraw.Draw(img)    # 创建绘图对象
        num_boxes = 0                  # 初始化边界框计数
        
        for field in data["form_fields"]:
            if field["page_number"] == page_number:  # 只处理指定页面的字段
                entry_box = field['entry_bounding_box']   # 获取输入框边界框
                label_box = field['label_bounding_box']   # 获取标签边界框
                # 在输入边界框上绘制红色矩形，在标签上绘制蓝色矩形
                draw.rectangle(entry_box, outline='red', width=2)   # 红色：输入区域
                draw.rectangle(label_box, outline='blue', width=2)  # 蓝色：标签区域
                num_boxes += 2  # 增加计数（每个字段两个框）
        
        img.save(output_path)  # 保存验证图像
        print(f"已创建验证图像: {output_path}，包含 {num_boxes} 个边界框")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: create_validation_image.py [页码] [fields.json 文件] [输入图像路径] [输出图像路径]")
        sys.exit(1)
    page_number = int(sys.argv[1])
    fields_json_path = sys.argv[2]
    input_image_path = sys.argv[3]
    output_image_path = sys.argv[4]
    create_validation_image(page_number, fields_json_path, input_image_path, output_image_path)
