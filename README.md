# Vieboo

## 安装指南

1. 安装 [Python 2.7](http://www.python.org/download/), pip

2. 安装虚拟环境 

	首先安装 virtualenv
	
		# pip install virtualenv
	
	创建虚拟环境
	
		$ virtualenv venv
		
	等待几分钟，安装完毕后运行(Windows)
	
		$ venv\Scripts\activate.bat
		
	或者(Linux)
	
		$ source venv/bin/activate
		
	然后在虚拟环境中安装第三方库
	
		pip install -r requirements.txt


	打开 venv/lib/python2.7/site-packages/flaskext/themes.py 找到 333 行，将：
	
		if USING_BLUEPRINTS and not self.as_blueprint:
	
	改为：
	
		if USING_BLUEPRINTS and self.as_blueprint:

2. 安装 [MariaDB](https://downloads.mariadb.org/mariadb/) 或者 [MySQL](http://dev.mysql.com/downloads/mysql/) 环境  
安装时请务必选择数据库编码为 **utf8** ，并设置 **root 密码**。
 
3. 创建数据库
进入数据库控制台输入以下代码创建数据库

		CREAT DATABASE microblog;
4. 修改项目配置文件

	打开 microblog/config.py，将 DB_PASSWORD = 'whypro' 中的 'whypro' 修改为您的数据库 **root 密码**
5. 运行服务器

		python runserver.py
7. 初始化数据库

	打开 http://localhost:5000/admin/install/ 自动初始化数据库，成功后将跳转至首页

8. 注册一个账号体验吧！


------
By whypro  
2014-01
