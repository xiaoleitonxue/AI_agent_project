# 智扫通机器人智能客服系统

## 📋 项目简介

智扫通机器人智能客服是一个基于 LangChain 和 ReAct 模式的智能问答系统，专门用于提供扫地机器人和扫拖一体机器人的专业咨询服务。该系统结合了 RAG（检索增强生成）技术、向量数据库和多工具调用能力，能够为用户提供准确、专业的机器人使用建议、故障排除、维护保养等信息。

## 🌟 核心特性

- **ReAct 推理模式**：采用思考→行动→观察→再思考的循环推理机制
- **RAG 检索增强**：基于 Chroma 向量数据库的知识检索与总结
- **多工具集成**：支持天气查询、用户定位、数据获取等多种工具
- **个性化报告**：可生成用户专属的机器人使用情况报告
- **流式响应**：支持实时流式输出，提升用户体验
- **中间件架构**：具备工具监控、日志记录和动态提示词切换功能

## 🏗️ 技术架构

### 核心技术栈

- **前端界面**：Streamlit
- **AI 框架**：LangChain, LangGraph
- **大语言模型**：通义千问 (Qwen3-Max)
- **嵌入模型**：DashScope Text Embedding v4
- **向量数据库**：Chroma DB
- **配置管理**：YAML

### 系统架构图

mermaid graph TB A[用户界面 Streamlit] --> B[ReAct Agent] B --> C[LLM Qwen3-Max] B --> D[工具集] D --> E[RAG 检索服务] D --> F[天气查询工具] D --> G[用户信息工具] D --> H[外部数据工具] E --> I[Chroma 向量库] I --> J[知识库文档] B --> K[中间件层] K --> L[工具监控] K --> M[日志记录] K --> N[动态提示词]

## 📁 项目结构

AI_agent_project/ ├── agent/ # Agent 核心模块 │ ├── react_agent.py # ReAct Agent 主类 │ └── tools/ # 工具定义 │ ├── agent_tools.py # 各种工具函数 │ └── middleware.py # 中间件处理 ├── rag/ # RAG 检索模块 │ ├── rag_service.py # RAG 服务类 │ └── vector_store.py # 向量存储服务 ├── model/ # 模型工厂 │ └── factory.py # 聊天模型和嵌入模型工厂 ├── config/ # 配置文件 │ ├── agent.yml # Agent 配置 │ ├── chroma.yml # Chroma 数据库配置 │ ├── prompts.yml # 提示词路径配置 │ └── rag.yml # RAG 模型配置 ├── prompts/ # 提示词模板 │ ├── main_prompt.txt # 主提示词 │ ├── rag_summarize.txt # RAG 总结提示词 │ └── report_prompt.txt # 报告生成提示词 ├── data/ # 数据目录 │ ├── external/ # 外部数据 │ │ └── records.csv # 用户使用记录 │ ├── 扫地机器人100问.pdf # 知识库文档 │ ├── 扫地机器人100问2.txt # 知识库文档 │ ├── 扫拖一体机器人100问.txt # 知识库文档 │ ├── 故障排除.txt # 知识库文档 │ ├── 维护保养.txt # 知识库文档 │ └── 选购指南.txt # 知识库文档 ├── chroma_db/ # Chroma 向量数据库存储 ├── logs/ # 日志文件 ├── utils/ # 工具类 │ ├── config_handler.py # 配置加载器 │ ├── file_handler.py # 文件处理器 │ ├── logger_handler.py # 日志处理器 │ ├── path_tool.py # 路径工具 │ └── prompt_loader.py # 提示词加载器 ├── app.py # Streamlit 应用入口 └── md5.txt # 文件 MD5 校验存储

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip 包管理器

### 安装依赖

bash 
pip install streamlit langchain langchain-community
langchain-chroma langgraph
pip install dashscope pyyaml

### 配置说明

1. **模型配置** (`config/rag.yml`)

    yaml 
    chat_model_name: qwen3-max 
    embedding_model_name: text-embedding-v4

2. **向量数据库配置** (`config/chroma.yml`)

    yaml collection_name: agent persist_directory: chroma_db k: 3 data_path: data md5_hex_store: md5.txt allow_knowledge_file_type: ["txt", "pdf"] chunk_size: 200 chunk_overlap: 20 separators: ["\n\n", "\n", ".", "!", "?", "。", "！", "？", "|", ""]

3. **提示词配置** (`config/prompts.yml`)

    yaml main_prompt_path: prompts/main_prompt.txt rag_summarize_prompt_path: prompts/rag_summarize.txt report_prompt_path: prompts/report_prompt.txt

### 初始化向量数据库

在首次运行前，需要构建向量数据库：

bash python rag/vector_store.py

这将读取 `data/` 目录下的 PDF 和 TXT 文件，进行文本分割并存储到 Chroma 向量数据库中。

### 启动应用

bash streamlit run app.py

访问 `http://localhost:8501` 即可使用智能客服系统。

## 🛠️ 核心功能模块

### 1. ReAct Agent

采用 ReAct (Reasoning + Acting) 模式，实现智能推理和工具调用的结合：

- **思考**：分析用户需求，判断是否需要调用工具
- **行动**：选择合适的工具并执行
- **观察**：获取工具返回结果
- **再思考**：基于结果决定下一步操作

### 2. RAG 检索服务

基于向量相似度的知识检索系统：

- 使用 DashScope 嵌入模型将文本转换为向量
- 通过 Chroma 数据库进行相似度搜索
- 结合 LLM 对检索结果进行智能总结

### 3. 工具集

系统提供以下工具：

| 工具名称                      | 功能描述       | 参数             |
|---------------------------|------------|----------------|
| `rag_summarize`           | 从向量库检索专业知识 | query: 检索词     |
| `get_weather`             | 获取城市天气信息   | city: 城市名      |
| `get_user_location`       | 获取用户所在城市   | 无              |
| `get_user_id`             | 获取用户唯一标识   | 无              |
| `get_current_month`       | 获取当前月份     | 无              |
| `fetch_external_data`     | 获取用户使用记录   | user_id, month |
| `fill_context_for_report` | 注入报告生成上下文  | 无              |

### 4. 中间件系统

- **工具监控** (`monitor_tool`)：记录工具调用日志
- **模型日志** (`log_before_model`)：记录模型调用前的状态
- **动态提示词** (`report_prompt_switch`)：根据场景切换提示词

## 📊 使用场景

### 场景 1：产品咨询

用户：小户型适合哪种扫地机器人？ 系统：调用 rag_summarize 工具检索选购指南，生成专业建议

### 场景 2：故障排除

用户：扫地机器人总是迷路怎么办？ 系统：检索故障排除知识库，提供解决方案

### 场景 3：维护保养

用户：在我的地区气温下如何保养扫地机器人？ 
系统：
调用 get_user_location 获取用户城市
调用 get_weather 获取天气信息
调用 rag_summarize 检索保养建议
综合信息生成个性化建议

### 场景 4：生成使用报告

用户：生成我6月份的使用报告 
系统：
调用 get_user_id 获取用户ID
调用 fill_context_for_report 注入报告上下文
调用 fetch_external_data 获取使用记录
切换至报告提示词模板
生成 Markdown 格式的使用报告

## 🔧 开发指南

### 添加新工具

1. 在 `agent/tools/agent_tools.py` 中定义工具函数
2. 使用 `@tool` 装饰器并添加描述
3. 在 `react_agent.py` 中注册工具

python @tool(description="工具功能描述") def new_tool(param: str) -> str: """工具实现""" return result

### 自定义提示词

1. 在 `prompts/` 目录下创建新的提示词文件
2. 在 `config/prompts.yml` 中添加路径配置
3. 在代码中通过 `load_system_prompts()` 加载

### 扩展知识库

1. 将新的 PDF 或 TXT 文件放入 `data/` 目录
2. 运行 `python rag/vector_store.py` 重新构建向量库
3. 系统会自动检测新文件并添加到向量数据库

## 📝 日志系统

日志文件存储在 `logs/` 目录下，按日期命名：

- **控制台日志**：INFO 级别及以上
- **文件日志**：DEBUG 级别及以上

日志格式：
%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s

## ⚠️ 注意事项

1. **API Key 配置**：需要在环境变量中配置 DashScope API Key
   bash export DASHSCOPE_API_KEY=your_api_key
2. **文件编码**：TXT 文件必须使用 UTF-8 编码

3. **配置文件扩展名**：所有配置文件使用 `.yml` 扩展名，而非 `.yaml`

4. **向量库更新**：修改知识库文件后，建议删除 `chroma_db/` 目录并重新构建

5. **工具调用限制**：Agent 最多进行 5 次工具调用，超过后将返回"我不知道"

## 🐛 常见问题

### Q1: 向量库构建失败
**A**: 检查 `data/` 目录中的文件是否为 UTF-8 编码，确认文件格式为 PDF 或 TXT。

### Q2: 模型调用失败
**A**: 确认已正确配置 DashScope API Key，并检查网络连接。

### Q3: Streamlit 启动失败
**A**: 确认已安装所有依赖包，特别是 `streamlit` 和 `langchain` 相关包。

## 📄 许可证

本项目仅供学习和研究使用。

## 👥 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**智扫通机器人智能客服** - 让扫地机器人使用更智能、更便捷！
