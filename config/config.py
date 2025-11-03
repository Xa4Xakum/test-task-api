

class Config():
    '''Настройки бота'''

    @property
    def db_connection(self) -> str:
        '''Подключение к бд. Используется sqlite, так что .env можно не прописывать'''
        return f'sqlite+aiosqlite:///config/Xakum.db'

    @property
    def secret_key(self) -> str:
        '''Секретный ключ для авторизации'''
        return 'super-secret-auth-key'
