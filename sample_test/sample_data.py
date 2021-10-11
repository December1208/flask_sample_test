from typing import List, Union

import sqlalchemy


class SampleData:
    def __init__(self, model, data, db):
        self._model: callable = model
        self._data: dict = data
        self._instance = None
        self._db = db
        self._inspector = sqlalchemy.inspect(self._db.engine)

    def create_instance(self):
        if self._instance:
            return self._instance.id
        self._instance = self._model()

        columns = self._inspector.get_columns(self._model.__tablename__)
        for column in columns:
            column_name = column.get('name')
            column_nullable = column.get('nullable')
            column_type = column.get("type")
            column_default = column.get('default')
            if column_name == 'id':
                continue
            if column_name in self._data:
                data = self._data.get(column_name)
                if isinstance(column_type, self._db.Integer) and \
                        isinstance(data, SampleData):
                    fk = data.create_instance()
                    setattr(self._instance, column_name, fk)
                elif isinstance(data, (SimpleDataField, ComplexDataField)):
                    setattr(self._instance, column_name, str(data))
                else:
                    setattr(self._instance, column_name, data)
            assert column_name in self._data or column_nullable is True or column_default is not None, \
                f'{self._model.__name__.lower()} 的非空字段 {column_name} 不能为空'

        self._db.session.add(self._instance)
        self._db.session.flush()

        return self._instance.id

    def relation_model(self):
        result = [self]
        for key, value in self.data.items():
            if isinstance(value, SampleData):
                result.extend(value.relation_model())
        return result

    def init_instance(self):
        self._instance = None

    def load_instance(self):
        self._instance = self._db.session.merge(self._instance)

        return self._instance

    def __getattr__(self, item):
        self._instance = self.load_instance()
        return getattr(self._instance, item, None)

    def __setattr__(self, key, value):
        if key in ('_model', '_data', '_instance'):
            super(SampleData, self).__setattr__(key, value)
            return

        self._instance = self.load_instance()
        setattr(self._instance, key, value)


class SimpleDataField:
    def __init__(self, sample_data: SampleData, field: str):
        """
        :param format_: 格式化字符串 ex: test_{}_format
        :param values: 格式化字符串中需要的数据，ex: [(SampleData, field)]
        """
        self._sample_data = sample_data
        self._field = field

    def __str__(self):

        self._sample_data.create_instance()
        return getattr(self._sample_data, self._field)

    def init_instance(self):
        self._sample_data.init_instance()


class ComplexDataField:
    def __init__(self, data: Union[dict, list, tuple, int, float, bool, str]):
        """
        :param data: 数据,
        """
        self.data = data
        self.relation: List[Union[SampleData, SimpleDataField]] = []

    def __str__(self):

        return json.dumps(self.data, cls=SampleTestJSONEncoder)

    def _relation_simple_data(self, obj):
        if isinstance(obj, (str, float, int, bool)):
            return

        if isinstance(obj, SimpleDataField):
            self.relation.append(obj)

        if isinstance(obj, dict):
            for key, value in obj.items():
                self._relation_simple_data(key)
                self._relation_simple_data(value)
        if isinstance(obj, (list, tuple)):
            for item in obj:
                self._relation_simple_data(item)

    def init_instance(self):
        for item in self.relation:
            item.init_instance()

