## Ai对话使用文档

- 通义千问大模型（Plus 版本）
- 接入方式：OpenAPI 接口调用

- **前端**：Vue3 + ElementPlus + Axios，构建用户对话界面
- **后端**：FastAPI，提供 API 接口，转发请求给通义千问并返回结果
- **数据库**：MySQL，用于存储用户聊天记录

## 如何运行



### 数据库：

创建数据库aiproject，创建chat_history表。

```mysql
CREATE TABLE chat_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id VARCHAR(64),
  message TEXT,
  reply TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 后端：

配置数据库库名、用户名、密码。

![image-20250724171812151](https://ikun-jpg.oss-cn-beijing.aliyuncs.com/image-20250724171812151.png)

将DASHSCOPE_API_KEY变量名换成自己的key

```python
DASHSCOPE_API_KEY = "在这里写上你的key"
```



在后端文件当前目录下的终端执行命令`uvicorn main:app --reload`

### 前端：

在前端文件当前目录下的终端执行命令`npm run install`安装依赖，执行`npm run dev`启动项目

在浏览器中访问`localhost:5173`，输入问题后回车，即可看到返回结果。



整体的逻辑明白，但是由于不太熟悉这个框架，所以后端框架部分使用Ai生成，前端Vue中的css使用Ai生成。

