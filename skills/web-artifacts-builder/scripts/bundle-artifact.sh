#!/bin/bash
set -e

echo "📦 正在将React应用打包为单个HTML工件..."

# 检查是否在项目目录中
if [ ! -f "package.json" ]; then
  echo "❌ 错误: 未找到package.json。请在项目根目录运行此脚本。"
  exit 1
fi

# 检查是否存在index.html
if [ ! -f "index.html" ]; then
  echo "❌ 错误: 在项目根目录中未找到index.html。"
  echo "   此脚本需要一个index.html作为入口点。"
  exit 1
fi

# 安装打包依赖项
echo "📦 正在安装打包依赖项..."
pnpm add -D parcel @parcel/config-default parcel-resolver-tspaths html-inline

# 创建带tspaths解析器的Parcel配置
if [ ! -f ".parcelrc" ]; then
  echo "🔧 正在创建带路径别名支持的Parcel配置..."
  cat > .parcelrc << 'EOF'
{
  "extends": "@parcel/config-default",
  "resolvers": ["parcel-resolver-tspaths", "..."]
}
EOF
fi

# 清理之前的构建
echo "🧹 正在清理之前的构建..."
rm -rf dist bundle.html

# 使用Parcel构建
echo "🔨 正在使用Parcel构建..."
pnpm exec parcel build index.html --dist-dir dist --no-source-maps

# 将所有内容内联到单个HTML中
echo "🎯 正在将所有资源内联到单个HTML文件中..."
pnpm exec html-inline dist/index.html > bundle.html

# 获取文件大小
FILE_SIZE=$(du -h bundle.html | cut -f1)

echo ""
echo "✅ 打包完成！"
echo "📄 输出文件: bundle.html ($FILE_SIZE)"
echo ""
echo "现在您可以在大型语言模型对话中使用这个单个HTML文件作为工件。"
echo "本地测试方法: 在浏览器中打开bundle.html"