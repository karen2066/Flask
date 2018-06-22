from functools import wraps

from flask import session, redirect, url_for


def is_login(view_func):
    @wraps(view_func)
    def check_login(*args, **kwargs):
        # 验证登录
        if 'user_id' in session:  # 成功
            return view_func(*args, **kwargs)
        else:  # 失败
            return redirect(url_for('user.login'))
        return check_login()


