from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ValidationError
from . import models


class PulishModelSerializer(ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ('name', 'address')


class BookModelSerializer(ModelSerializer):

    # 了解：该方式设置的序列化字段，必须fields中声明
    # publish_address = SerializerMethodField()
    # def get_publish_address(self, obj):
    #     return obj.publish.address

    # 自定义连表深度 - 子序列化方式
    publish = PulishModelSerializer()
    # publish = '1'

    class Meta:
        # 序列化类关联的model类
        model = models.Book
        # 参与序列化的字段
        fields = ['name','publish_name', 'author_list', 'publish']

        # 了解知识点
        # 所有字段
        # fields = '__all__'
        # 与fields不共存，exclude排除哪些字段
        # exclude = ['id']
        # 自动连表深度
        # depth = 1


class BookModelDeserializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = ['name','price', 'img', 'publish', 'authors']
        # extra_kwargs用来完成反序列化字段的系统校验规则
        extra_kwargs = {
            'name': {
                'required': True,
                'min_length':1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短了'
                }
            }
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


    # ModelSerializer类已经帮我们实现了 create与update方法


""""
1 fields中设置悵经与反序列化字段
2 extra_kwargs划分只序列化或只反序列化字段
    write_only：只反序列化
    read_only：只序列化
    自定义字段默认只序列化(read_only)
3 设置反序列化所需的系统、局部钩子、全局钩子等校验规则
"""
from rest_framework.serializers import ListSerializer


# 重点： ListSerializer与ModelSerializer建立关联的是：
# ModelSerializer的Meta类的 - list_serializer_class
class V2BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        print(instance)     # 要更新的对象
        print(validated_data)   # 更新的对象对应的数据们
        print(self.child)   # 服务的模型序列化类 - V2BookModelSerializer
        for index, obj in enumerate(instance):
            print(obj, validated_data[index])
            self.child.update(obj, validated_data[index])
        return instance

class V2BookModelSerializer(ModelSerializer):

    class Meta:
        # 序列化类关联的model类
        model = models.Book
        # 参与序列化的字段
        fields = ['name','price','publish_name', 'img', 'author_list', 'publish_name', 'publish', 'authors']
        # 群改，需要设置自定义ListSerializer，重写尹改updata方法
        list_serializer_class = V2BookListSerializer

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
        print('钩子用：%s'%self.context.get('request'))
        publish = attrs.get('publish')
        name = attrs.get('name')
        if models.Book.objects.filter(name=name, publish=publish):
            raise ValidationError({'book': '该书名已存在'})
        return attrs
