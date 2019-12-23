#### 登录接口

请求方式：POST

请求地址：/api/user/auth/login/

请求参数：
    
    u_username string 账号
    u_password string 密码

响应成功：

    {
        'code': 200,
        'msg': '请求成功',
        'data': {
            'token': token
        }
    }

响应失败：

    {
        'code': 1001,
        'msg': '参数有问题',
        'data': {
            'username': '用户名不存在'
        }
    }

响应参数：

    username string 账号
    password string 密码