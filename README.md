基于 Streamlit + 通义千问（DashScope）+ Chroma 向量数据库构建的个人知识库问答助手，支持上传 TXT 文件构建知识库，并基于 RAG（检索增强生成）技术实现智能问答，同时保留对话历史。
功能特点
📤 支持 TXT 文件上传，自动拆分文本并存储到向量数据库
🔍 基于向量检索的知识库问答，优先参考上传的资料回答
📝 保留对话历史，上下文感知的智能回答
⚡ 流式回答输出，提升交互体验
🔒 基于 MD5 校验避免重复上传相同内容
环境要求
Python 3.8+
阿里云 DashScope API 密钥（需要开通通义千问服务）
安装步骤
1. 克隆仓库
bash
运行
git clone https://github.com/your-username/rag-knowledge-base.git
cd rag-knowledge-base
2. 安装依赖
创建并激活虚拟环境（可选但推荐），然后安装依赖：
bash
运行
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
3. 配置依赖包
创建 requirements.txt 文件，包含以下内容：
txt
streamlit>=1.30.0
langchain-core>=0.1.0
langchain-community>=0.0.0
langchain-chroma>=0.1.0
chromadb>=0.4.0
python-dotenv>=1.0.0
hashlib>=2.0
dashscope>=1.14.0
4. 配置 API Key
修改以下文件中的 DASHSCOPE_API_KEY 为你的阿里云 DashScope 密钥：
rag.py
knowledge_base.py
🔐 建议将 API Key 放到环境变量中，避免硬编码（生产环境推荐使用 .env 文件）。
使用方法
1. 运行文件上传服务（构建知识库）
bash
运行
streamlit run RAG/app_file_uploader.py
打开浏览器访问输出的本地地址（通常是 http://localhost:8501）
上传 TXT 格式的文件，系统会自动拆分文本、生成向量并存储到 Chroma 数据库
2. 运行问答服务
bash
运行
streamlit run RAG/app_qa.py
在聊天框中输入问题，助手会基于上传的知识库内容回答问题
支持多轮对话，会保留历史对话上下文
项目结构
plaintext
RAG/
├── app_file_uploader.py    # 文件上传界面，用于构建知识库
├── app_qa.py               # 问答界面，基于RAG的智能问答
├── rag.py                  # RAG核心逻辑，构建检索-生成链
├── knowledge_base.py       # 知识库服务，处理文件上传、文本拆分、向量存储
├── vector_stores.py        # 向量数据库服务，封装Chroma操作
├── file_history_store.py   # 对话历史存储，基于文件的聊天记录管理
├── config_date.py          # 项目配置文件（向量库、文本拆分、会话等配置）
├── md5.text                # MD5校验文件，避免重复上传（自动生成）
└── chroma_db/              # Chroma向量数据库存储目录（自动生成）
核心配置说明（config_date.py）
配置项	说明	默认值
md5_path	MD5 校验文件路径	./md5.text
collection_name	Chroma 集合名称	rag
persist_directory	向量数据库持久化目录	./chroma_db
chunk_size	文本拆分块大小	1000
chunk_overlap	文本块重叠长度	100
separators	文本拆分分隔符	中文 / 英文标点
max_split_chat	最小拆分长度	100
similarity_threshold	检索相似度阈值	2
session_config	会话配置	session_id: user_01
技术栈
前端 / 交互：Streamlit
大模型：通义千问（qwen3-max）
嵌入模型：通义千问嵌入模型（qwen-embed-v1.0）
向量数据库：Chroma
RAG 框架：LangChain
注意事项
确保你的 DashScope API Key 有足够的额度，避免调用失败
仅支持 TXT 文件上传，如需支持其他格式（PDF/Word），需扩展文件解析逻辑
对话历史存储在本地 chat_history 目录下，如需多用户支持，需修改 session_id 生成逻辑
向量数据库默认存储在本地，如需部署到服务器，需考虑数据持久化和备份
扩展方向
支持更多文件格式（PDF、Word、Markdown 等）
添加用户认证，支持多用户隔离
优化检索策略（如混合检索、关键词 + 向量检索）
增加知识库管理功能（删除 / 修改文件、查看已上传文件）
部署到云服务器（如阿里云、腾讯云），支持公网访问
