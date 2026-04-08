# MultiAI Hub

多AI员工管理系统 - 270+角色库、项目制工作流、飞书集成

## 功能特性

- **角色库**: 270+预定义AI角色 (程序员、设计师、产品经理、文案等)
- **项目制工作流**: 基于项目的任务分配与协作
- **飞书集成**: 消息推送、文档同步、日程管理
- **多模型支持**: 集成多个LLM模型 (GPT、Claude、Claude、本地模型等)
- **任务追踪**: 项目进度、任务状态、工作时间记录
- **知识库**: 团队知识沉淀与共享

## 系统架构

```
MultiAI Hub
├── 角色管理 (Role Manager)
│   ├── 角色库 (270+ 预定义角色)
│   ├── 角色模板
│   └── 自定义角色
├── 项目管理 (Project Manager)
│   ├── 项目创建与配置
│   ├── 任务分配
│   └── 进度追踪
├── 工作流引擎 (Workflow Engine)
│   ├── 任务调度
│   ├── 依赖管理
│   └── 状态机
└── 集成层 (Integrations)
    ├── 飞书 (Feishu)
    ├── GitHub
    ├── Obsidian
    └── 自定义钩子
```

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 配置

编辑 `config.yaml` 配置API密钥和集成设置。

### 使用示例

```python
from multiai_hub import MultiAIHub

# 初始化系统
hub = MultiAIHub()

# 创建项目
project = hub.create_project(
    name="Web开发项目",
    description="使用React和Node.js开发Web应用"
)

# 分配任务给角色
task = project.add_task(
    title="设计数据库架构",
    role="backend_architect",
    priority="high"
)

# 启动工作流
hub.run_workflow(project)
```

## 角色库示例

- **技术类**: frontend_dev, backend_dev, fullstack_dev, devops, data_scientist
- **设计类**: ui_designer, ux_designer, product_designer, graphic_designer
- **产品类**: product_manager, business_analyst, project_manager
- **营销类**: content_writer, copywriter, seo_specialist, social_media_manager
- **其他**: consultant, researcher, analyst, translator

## 飞书集成

### 功能

- 消息推送: 任务完成、项目更新
- 文档同步: 自动同步项目文档到飞书
- 日程管理: 同步任务截止日期到飞书日历

### 配置

```yaml
feishu:
  app_id: "your_app_id"
  app_secret: "your_app_secret"
  webhook_url: "your_webhook_url"
  enabled: true
```

## 项目状态

- [x] 核心架构设计
- [x] 角色库 (270+ 角色定义)
- [ ] 工作流引擎实现
- [ ] 飞书集成
- [ ] GitHub 集成
- [ ] Obsidian 集成
- [ ] Web UI 开发
- [ ] 测试与文档

## 迁移状态

- [x] OpenClaw配置已识别
- [x] 角色库已提取
- [ ] 项目数据迁移
- [ ] 飞书集成配置迁移
- [ ] 测试与验证

## 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License
