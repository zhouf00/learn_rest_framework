from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

from api_v3 import models


# 重点： ListSerializer与ModelSerializer建立关联的是：
# ModelSerializer的Meta类的 - list_serializer_class
class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        # print(instance)     # 要更新的对象
        # print(validated_data)   # 更新的对象对应的数据们
        # print(self.child)   # 服务的模型序列化类 - BookModelSerializer
        for index, obj in enumerate(instance):
            # print(obj, validated_data[index])
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializer(ModelSerializer):

    class Meta:
        # 序列化类关联的model类
        model = models.Book
        # 参与序列化的字段
        fields = ['name','price','publish_name', 'img', 'author_list', 'publish', 'authors']
        # 群改，需要设置自定义ListSerializer，重写尹改updata方法
        list_serializer_class = BookListSerializer

        extra_kwargs = {
            'name': {
                'required': True,
                'min_length': 2,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短了'
                }
            },
            'publish': {
                'write_only': True
            },
            'authors': {
                'write_only': True
            },
            'img': {
                'read_only': True
            },

        }

    # 局部钩子
    def validate_name(self, value):
        # 书名不能包含 g 字符
        if 'g' in value.lower():
            raise ValidationError('该《%s》书不能出版'%value)
        return value

    # 全局钩子
    def validate(self, attrs):
        publish = attrs.get('publish')
        name = attrs.get('name')
        if models.Book.objects.filter(name=name, publish=publish):
            raise ValidationError({'book': '该书名已存在'})
        return attrs
