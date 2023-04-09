from pymongo import MongoClient

class Database:
    __client = None
    __connection = None
    __host = 'localhost'
    __port = 27017
    __db = 'flask'
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def connect(self):
        Database.__client = MongoClient(f'mongodb://{self.__host}:{self.__port}')
        Database.__connection = Database.__client[Database.__db]

    @property
    def db(self):
        if not Database.__connection:
            raise RuntimeError('No database connection available.')
        return Database.__connection

    @property
    def engine(self):
        if not Database.__client:
            raise RuntimeError('No database engine initialized.')
        return Database.__client