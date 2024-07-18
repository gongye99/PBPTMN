import traceback
import pymysql
from databaseconfig import databaseConfig


class MySqlDBClient(object):

    def __init__(self, request=None):
        # 初始化方法，设置数据库连接配置和一些实例变量
        self.config = {
            'host': databaseConfig['db_host'],
            'port': databaseConfig['db_port'],
            'database': databaseConfig['db_name'],
            'user': databaseConfig['db_user'],
            'password': databaseConfig['db_password'],
            'charset': 'utf8',
        }
        self._conn = None  # 用于存储数据库连接对象
        self._cursor = None  # 用于存储数据库游标对象
        self.request = request  # 存储请求对象

    def fetchall(self, sql):
        # 执行 SELECT 查询并返回结果，转换为字典格式
        self._connect()
        self._cursor = self._conn.cursor()
        self._cursor.execute(sql)
        fetchTuple = self._cursor.fetchall()
        result = self._convertFetchResultToDict(fetchTuple)
        self._close()
        return result

    def insert(self, sql, data):
        # 执行 INSERT 操作，返回插入的最后一行 ID
        self._connect()
        self._cursor = self._conn.cursor()
        self._cursor.execute(sql, data)
        self._conn.commit()
        lastId = self._cursor.lastrowid
        self._close()
        return lastId

    def execute(self, sql, data):
        # 执行 UPDATE、DELETE 等操作，返回1表示执行成功
        self._connect()
        self._cursor = self._conn.cursor()
        self._cursor.execute(sql, data)
        self._conn.commit()
        self._close()
        return 1

    def _convertFetchResultToDict(self, fetchTuple):
        # 将 SELECT 查询的结果转换为字典格式
        if not fetchTuple:
            return []

        description = self._cursor.description
        result = [
            {description[i][0]: fetchItem[i] for i in range(len(fetchItem))}
            for fetchItem in fetchTuple
        ]
        return result

    def _connect(self):
        # 建立数据库连接
        try:
            self._conn = pymysql.connect(
                **self.config
            )
        except:
            pass

    def _close(self):
        # 关闭数据库连接和游标
        try:
            if self._cursor:
                self._cursor.close()
            if self._conn:
                self._conn.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def pageSizeToLimitOffset(page, size):
        # 根据页码和页面大小计算查询的 LIMIT 和 OFFSET
        if type(page) != int or type(size) != int or size <= 0:
            return 0, 0
        limit = size
        offset = (page - 1) * size if page > 1 else 0
        return limit, offset
