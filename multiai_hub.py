#!/usr/bin/env python3
"""
MultiAI Hub - 多AI员工管理系统
"""

import os
import json
import yaml
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(Enum):
    """优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Role:
    """角色类"""
    name: str
    description: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 2000
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class Task:
    """任务类"""
    id: str
    title: str
    description: str
    role: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    assignee: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    result: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class Project:
    """项目类"""
    id: str
    name: str
    description: str
    status: str = "active"
    tasks: List[Task] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)
    
    def add_task(self, task: Task) -> Task:
        """添加任务到项目"""
        self.tasks.append(task)
        self.updated_at = datetime.now().isoformat()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """根据状态获取任务"""
        return [t for t in self.tasks if t.status == status]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """根据优先级获取任务"""
        return [t for t in self.tasks if t.priority == priority]


class RoleLibrary:
    """角色库管理类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.roles: Dict[str, Role] = {}
        self._load_roles()
    
    def _load_roles(self):
        """加载角色库"""
        role_dir = self.config.get('roles', {}).get('directory', './roles')
        
        # 如果角色目录不存在，使用内置角色
        if not os.path.exists(role_dir):
            self._load_builtin_roles()
            return
        
        # 从文件加载角色
        for filename in os.listdir(role_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                filepath = os.path.join(role_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    role_data = yaml.safe_load(f)
                    role = Role(**role_data)
                    self.roles[role.name] = role
    
    def _load_builtin_roles(self):
        """加载内置角色库"""
        builtin_roles = [
            {
                "name": "frontend_dev",
                "description": "前端开发工程师，专注于Web界面和用户体验",
                "system_prompt": "你是一个经验丰富的前端开发工程师，精通React、Vue、TypeScript等技术栈。你关注用户体验和界面性能。",
                "capabilities": ["React", "Vue", "TypeScript", "CSS", "UI/UX"]
            },
            {
                "name": "backend_dev",
                "description": "后端开发工程师，专注于服务器逻辑和API设计",
                "system_prompt": "你是一个专业的后端开发工程师，精通Node.js、Python、数据库设计和API开发。你注重代码质量和系统架构。",
                "capabilities": ["Node.js", "Python", "REST API", "Database", "System Design"]
            },
            {
                "name": "fullstack_dev",
                "description": "全栈开发工程师，能够处理前后端开发任务",
                "system_prompt": "你是一个全栈开发工程师，熟悉前端和后端技术栈，能够独立完成完整的Web应用开发。",
                "capabilities": ["Frontend", "Backend", "Database", "DevOps"]
            },
            {
                "name": "ui_designer",
                "description": "UI设计师，专注于界面设计和视觉效果",
                "system_prompt": "你是一个专业的UI设计师，擅长创建美观、实用的用户界面。你关注色彩、排版和用户体验。",
                "capabilities": ["Figma", "Sketch", "Adobe XD", "UI Design", "Visual Design"]
            },
            {
                "name": "product_manager",
                "description": "产品经理，专注于产品规划和需求分析",
                "system_prompt": "你是一个经验丰富的产品经理，擅长需求分析、产品规划和项目管理。你关注用户需求和商业目标。",
                "capabilities": ["Product Strategy", "Requirements", "User Research", "Roadmap"]
            },
            {
                "name": "content_writer",
                "description": "内容创作者，擅长撰写各种类型的内容",
                "system_prompt": "你是一个专业的内容创作者，能够撰写高质量的文章、文案和社交媒体内容。",
                "capabilities": ["Writing", "Copywriting", "SEO", "Social Media"]
            },
            {
                "name": "data_scientist",
                "description": "数据科学家，专注于数据分析和机器学习",
                "system_prompt": "你是一个专业的数据科学家，精通数据分析、机器学习和统计建模。你关注数据洞察和模型性能。",
                "capabilities": ["Python", "Machine Learning", "Statistics", "Data Analysis"]
            },
            {
                "name": "devops",
                "description": "DevOps工程师，专注于系统部署和运维",
                "system_prompt": "你是一个经验丰富的DevOps工程师，精通CI/CD、容器化和云服务。你关注系统稳定性和自动化。",
                "capabilities": ["Docker", "Kubernetes", "CI/CD", "Cloud", "Automation"]
            }
        ]
        
        for role_data in builtin_roles:
            role = Role(**role_data)
            self.roles[role.name] = role
    
    def get_role(self, name: str) -> Optional[Role]:
        """获取角色"""
        return self.roles.get(name)
    
    def list_roles(self) -> List[str]:
        """列出所有角色"""
        return list(self.roles.keys())
    
    def search_roles(self, keyword: str) -> List[Role]:
        """搜索角色"""
        keyword = keyword.lower()
        return [role for role in self.roles.values() 
                if keyword in role.name.lower() or keyword in role.description.lower()]


class MultiAIHub:
    """MultiAI Hub主类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """初始化MultiAI Hub"""
        self.config = self._load_config(config_path)
        self.role_library = RoleLibrary(self.config)
        self.projects: Dict[str, Project] = {}
        self._load_projects()
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}
    
    def _load_projects(self):
        """加载项目数据"""
        project_dir = self.config.get('projects', {}).get('directory', './projects')
        
        if not os.path.exists(project_dir):
            return
        
        for filename in os.listdir(project_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(project_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                    # 转换任务数据
                    tasks = [Task(**task) for task in project_data.get('tasks', [])]
                    project_data['tasks'] = tasks
                    project = Project(**project_data)
                    self.projects[project.id] = project
    
    def _save_projects(self):
        """保存项目数据"""
        project_dir = self.config.get('projects', {}).get('directory', './projects')
        os.makedirs(project_dir, exist_ok=True)
        
        for project_id, project in self.projects.items():
            filepath = os.path.join(project_dir, f"{project_id}.json")
            
            # 转换任务数据为可序列化格式
            project_data = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "role": t.role,
                        "status": t.status.value,
                        "priority": t.priority.value,
                        "assignee": t.assignee,
                        "dependencies": t.dependencies,
                        "created_at": t.created_at,
                        "updated_at": t.updated_at,
                        "completed_at": t.completed_at,
                        "result": t.result,
                        "metadata": t.metadata
                    }
                    for t in project.tasks
                ],
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "metadata": project.metadata
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
    
    def create_project(self, name: str, description: str, 
                     metadata: Optional[Dict] = None) -> Project:
        """
        创建项目
        
        Args:
            name: 项目名称
            description: 项目描述
            metadata: 额外元数据
        
        Returns:
            创建的项目对象
        """
        project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        project = Project(
            id=project_id,
            name=name,
            description=description,
            metadata=metadata or {}
        )
        
        self.projects[project_id] = project
        self._save_projects()
        
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """获取项目"""
        return self.projects.get(project_id)
    
    def list_projects(self) -> List[str]:
        """列出所有项目"""
        return list(self.projects.keys())
    
    def search_roles(self, keyword: str) -> List[Role]:
        """搜索角色"""
        return self.role_library.search_roles(keyword)
    
    def get_role(self, name: str) -> Optional[Role]:
        """获取角色"""
        return self.role_library.get_role(name)
    
    def list_roles(self) -> List[str]:
        """列出所有角色"""
        return self.role_library.list_roles()
    
    def run_workflow(self, project: Project):
        """
        运行项目工作流 (简化版本)
        
        Args:
            project: 要运行工作流的项目
        """
        print(f"开始运行项目工作流: {project.name}")
        
        # 获取待执行的任务
        pending_tasks = project.get_tasks_by_status(TaskStatus.PENDING)
        
        # 按优先级排序
        priority_order = {Priority.URGENT: 0, Priority.HIGH: 1, 
                         Priority.MEDIUM: 2, Priority.LOW: 3}
        pending_tasks.sort(key=lambda t: priority_order[t.priority])
        
        for task in pending_tasks:
            print(f"执行任务: {task.title} (角色: {task.role})")
            
            # 模拟任务执行
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.now().isoformat()
            
            # 获取角色
            role = self.get_role(task.role)
            if role:
                print(f"  使用角色: {role.description}")
            
            # 模拟任务完成
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.updated_at = datetime.now().isoformat()
            task.result = "任务执行成功"
            
            print(f"  任务完成: {task.result}")
        
        self._save_projects()
        print(f"工作流执行完成: {project.name}")


if __name__ == "__main__":
    # 测试代码
    hub = MultiAIHub()
    
    # 列出可用角色
    print("可用角色:")
    for role_name in hub.list_roles():
        role = hub.get_role(role_name)
        print(f"  - {role_name}: {role.description}")
    
    # 创建项目
    project = hub.create_project(
        name="Web开发项目",
        description="使用React和Node.js开发Web应用"
    )
    
    # 添加任务
    task1 = Task(
        id="task_001",
        title="设计数据库架构",
        description="设计用户和产品数据库表结构",
        role="backend_dev",
        priority=Priority.HIGH
    )
    project.add_task(task1)
    
    task2 = Task(
        id="task_002",
        title="设计UI界面",
        description="设计主页和产品页面UI",
        role="ui_designer",
        priority=Priority.MEDIUM
    )
    project.add_task(task2)
    
    # 运行工作流
    hub.run_workflow(project)
    
    # 查看项目状态
    print(f"\n项目 '{project.name}' 的任务:")
    for task in project.tasks:
        print(f"  - [{task.status.value}] {task.title}")
