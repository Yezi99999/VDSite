# VDSite - 现代化博客平台

VDSite 是一个基于 Vue.js 3 + Django REST Framework 构建的现代化博客平台，提供完整的文章发布、评论互动和用户认证功能。

## 🌟 特性

### 前端特性
- **现代化UI设计** - 响应式设计，支持移动端和桌面端
- **用户认证系统** - 完整的登录/注册/退出功能
- **文章管理** - 文章创建、编辑、删除和浏览
- **评论系统** - 支持文章评论和互动
- **访客模式** - 无需登录即可浏览公开内容
- **路由守卫** - 智能的页面访问权限控制

### 后端特性
- **RESTful API** - 基于 Django REST Framework 构建
- **用户认证** - Session-based 认证系统
- **数据模型** - 完整的文章、分类、评论数据模型
- **权限控制** - 细粒度的权限管理
- **CORS支持** - 跨域资源共享配置
- **CSRF保护** - 完整的安全防护机制

## 🏗️ 技术栈

### 前端技术
- **Vue.js 3** - 渐进式 JavaScript 框架
- **Vue Router 4** - 官方路由管理器
- **Pinia** - Vue.js 状态管理库
- **Axios** - HTTP 客户端库
- **Vue CLI** - 项目脚手架和构建工具

### 后端技术
- **Django 4.2** - Python Web 框架
- **Django REST Framework** - Web API 框架
- **SQLite** - 开发环境数据库
- **CORS Headers** - 跨域请求支持

## 📁 项目结构
VDSite/ 
├── backend/ # Django 后端项目
│ ├── VDSite/ # Django 项目配置
│ │ ├── settings.py # 项目设置
│ │ ├── urls.py # 主路由配置
│ │ └── wsgi.py # WSGI 入口
│ ├── blog/ # 博客应用
│ │ ├── models.py # 数据模型
│ │ ├── views.py # 视图函数
│ │ ├── serializers.py # 序列化器
│ │ └── urls.py # API 路由
│ ├── manage.py # Django 管理脚本
│ └── db.sqlite3 # 开发数据库
├── frontend/ # Vue.js 前端项目
│ ├── src/
│ │ ├── components/ # Vue 组件
│ │ ├── views/ # 页面视图
│ │ ├── stores/ # Pinia 状态管理
│ │ ├── services/ # API 服务
│ │ ├── router/ # 路由配置
│ │ └── App.vue # 根组件
│ ├── public/ # 静态资源
│ ├── package.json # 依赖配置
│ └── vue.config.js # Vue 配置
└── README.md # 项目文档


## 🚀 快速开始

### 环境要求

- Node.js 14+ 
- Python 3.8+
- pip (Python 包管理器)

### 后端启动

1. **进入后端目录**
   ```bash
   cd backend
创建虚拟环境（推荐）


```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
安装依赖


```bash
pip install django djangorestframework django-cors-headers pillow
```
数据库迁移


```bash
python manage.py migrate
```
创建超级用户（可选）


```bash
python manage.py createsuperuser
```
启动开发服务器


```bash
python manage.py runserver
```
后端服务将在 http://localhost:8000 运行

前端启动
进入前端目录
```bash
cd frontend
```
安装依赖


```bash
npm install
```
启动开发服务器


```bash
npm run serve
```
前端服务将在 http://localhost:8080 运行

## 🔧 配置说明
### 后端配置
在 `backend/VDSite/settings.py` 中主要配置：

数据库: SQLite（开发环境）
CORS设置: 允许前端域名访问
认证系统: Session-based 认证
API前缀: `/api/`
### 前端配置
在 `frontend/src/services/api.js` 中配置：
- API基础URL: `http://localhost:8000/api/`
- 请求超时: 10秒
- CSRF保护: 自动处理 CSRF token
## 📚 API 文档
### 认证接口
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户退出
- `GET /api/auth/check/` - 检查认证状态
### 文章接口
- `GET /api/posts/` - 获取文章列表
- `POST /api/posts/` - 创建文章（需登录）
- `GET /api/posts/{id}/` - 获取文章详情
- `PUT /api/posts/{id}/` - 更新文章（需登录）
- `DELETE /api/posts/{id}/` - 删除文章（需登录）
### 评论接口
- `GET /api/comments/` - 获取评论列表
- `POST /api/comments/` - 创建评论
- `POST /api/posts/{id}/add_comment/` - 为文章添加评论
### 分类接口
- `GET /api/categories/` - 获取分类列表
## 🎯 使用指南
### 访客浏览
1. 访问首页自动进入介绍页面
2. 点击"访客浏览"按钮浏览公开内容
3. 可以查看文章列表和文章详情
### 用户登录
1. 点击"登录账号"按钮进入登录页面
2. 输入用户名和密码进行登录
3. 登录后可发布文章和管理个人内容
### 文章管理
- 浏览文章: 所有用户可浏览已发布的文章
- 发布文章: 登录用户可创建新文章
- 编辑文章: 文章作者可编辑自己的文章
- 删除文章: 文章作者可删除自己的文章
### 评论功能
- 所有用户可在文章下方发表评论
- 评论需要管理员审核后才能显示
- 支持评论回复和互动
### 故障排除
#### 常见问题
1. CORS 错误

   - 检查后端 CORS 配置是否正确
   - 确认前端请求的域名在白名单中
2. CSRF 验证失败
   - 确保前端正确发送 CSRF token
   - 检查 Cookie 设置是否正确
3. API 请求超时
   - 确认后端服务是否正常运行
   - 检查网络连接和防火墙设置
4. 路由跳转问题
   - 检查路由配置是否正确
   - 确认认证状态管理逻辑

#### 调试技巧
- 查看浏览器开发者工具中的网络请求
- 检查后端 Django 控制台输出
- 使用 Vue Devtools 调试前端状态
### 🤝 贡献指南
欢迎提交 Issue 和 Pull Request 来改进项目！

#### 开发流程
1. Fork 本项目
2. 创建功能分支 (git checkout -b feature/AmazingFeature)
3. 提交更改 (git commit -m 'Add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 开启 Pull Request

### 📄 许可证
本项目采用 MIT 许可证, 详情请查看 [LICENSE](LICENSE) 文件。

🙏 致谢
感谢所有为这个项目做出贡献的开发者！
---
VDSite - 让博客创作更简单、更愉悦！ 🚀