#### 注册接口

请求方式：POST

请求地址：/api/user/auth/register/

请求参数：

    u_userName string 账号
    u_password string 密码
    u_password2 string 确认密码
    u_email string 邮箱

响应成功：

    {
        'code': 200,
        'msg': '请求成功',
        'data': {
            'user_id': user.id
        }
    }

响应失败：
    
    {
        'code': 101,
        'msg': '校验有问题',
        'data': {
            'username': '用户名太长'
        }
    }

响应参数：
    
    username string 账号
    password string 密码
    password2 string 确认密码
    email string 邮箱