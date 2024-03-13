# Django后端服务

## how to deploy

```shell
python manage.py runserver
```

## 工作目录

- myDjangoApp
  - settings.py
    - 配置后端服务，如允许CORS请求
  - urls.py
    - 配置允许访问的urls
    - 其url会连接到对应app中的views的响应
- manage.py
  - 用于启动服务等
- dataHandler
  - 自己创建的app
  - views.py
    - 编写url对应的响应
- data
  - 存放模型、label、resultlabel等数据

## 如何构建一个项目

```shell
# 创建新的项目
django-admin.py startproject my_project

# 创建新的App
# 在Django项目(my_project)的根目录下执行
python3 manage.py startapp my_app


# 启动Django中的开发服务器
# make new migrations
python3 manage.py makemigrations
 
# apply all migrations
python3 manage.py migrate
 
# run server
python3 manage.py runserver
```

## 常见问题

### 向后端post时，被防CSRF机制阻拦

- [solution](https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set)

### CORS跨域请求资源时，被阻拦

- 安装**`django-cors-headers`**

- ```bash
  pip install django-cors-headers
  ```
- 在settings.py中配置

- ```python
  # settings.py  
    
  INSTALLED_APPS = [  
      # ...  
      'corsheaders',  
      # ...  
  ]  
    
  MIDDLEWARE = [  
      # ...  
      'corsheaders.middleware.CorsMiddleware',
      "django.middleware.common.CommonMiddleware",
      # ...  
  ]  
    
  CORS_ALLOWED_ORIGINS = [  
      "http://localhost:8081",  # 允许来自前端应用的跨域请求  
  ]  
  ```


## 实现数据传输

### 请求模型数据和label数据

- vtkOBJImporter 读入本地obj模型
- 读取polydata
- 将polydata用base64编码为字符串，加上labeljson，一起发送给前端

### 接受上传的label数据并保存

- 将接受到的json保存在本地