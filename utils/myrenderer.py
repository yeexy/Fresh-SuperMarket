"""__author__ = 叶小永"""
from rest_framework.renderers import JSONRenderer


class MyJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 只要方法中使用return Response(data)时，render()方法会被调用，将data转换成json
        if data and isinstance(data, dict):
            code = data.pop('code', 200)
            msg = data.pop('msg', '请求成功')
            result = data.pop('data', data)
        elif not data:
            code = 200
            msg = '请求成功'
            result = {}
        elif not isinstance(data, dict):
            code = 200
            msg = '请求成功'
            result = data
        # 将响应状态码修改为200，让前端显示错误信息
        renderer_context['response'].status_code = 200

        res = {
            'code': code,
            'msg': msg,
            'data': result
        }
        return super().render(res)

