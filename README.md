# AI 面试题生成器

这是一个基于 Streamlit 和 DeepSeek API 开发的 AI 面试辅助工具。

用户可以输入岗位名称、岗位方向、公司类型和个人基础，系统会自动生成高频面试题、参考答案、自我介绍、项目经历包装建议和面试前复习清单。

## 功能介绍

- 支持输入岗位名称
- 支持选择岗位方向
- 支持选择面试难度
- 支持选择生成内容类型
- 支持调用 DeepSeek API 生成面试准备内容
- 支持下载生成结果为 txt 文件

## 技术栈

- Python
- Streamlit
- DeepSeek API
- OpenAI Python SDK
- python-dotenv

## 项目运行方式

1. 安装依赖

```bash
pip install -r requirements.txt