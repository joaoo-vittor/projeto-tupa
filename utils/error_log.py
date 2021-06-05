import os
from datetime import date, datetime


class ErrorLog:

    @classmethod
    def save_error_log(cls, dir, id_user, class_name, func_name, error):
        fname = f'{os.getcwd()}/errors/{dir}/id_{str(id_user)}.log'

        err = f'[{str(datetime.now())}] - usuario_id: {id_user}, name_class_error: {class_name}, name_func_error: {func_name}, body_error: {error}\n'

        with open(fname, 'a+') as f:
            f.write(err)
