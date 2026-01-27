import sys
from pypdf import PdfReader


# 大型语言模型 用于运行以确定 PDF 是否具有可填写表单字段的脚本。详见 forms.md。


reader = PdfReader(sys.argv[1])
if (reader.get_fields()):
    print("此 PDF 具有可填写的表单字段")
else:
    print("此 PDF 没有可填写的表单字段；你需要直观地确定数据输入位置")
