from rest_framework.serializers import ModelSerializer, SerializerMethodField

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