# -*- coding: utf-8 -*-
from flask.ext.principal import Permission, RoleNeed

# Flask-Principal 的两个问题：
# 1. 调用私有方法：send(current_app._get_current_object())
# 2. 信号绑定的是 identity_loaded 而不是 identity_changed，每次请求都要加载
admin = Permission(RoleNeed('admin'))