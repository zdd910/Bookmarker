from .models import User, Entry, Favorite, Setting, Tag, TagRelation
from rest_framework import serializers


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('url', 'title', 'thumbnail', 'created_at', 'belong')


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    entries = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='entry-detail')
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'created_at', 'is_public', 'created_by', 'entries', 'entries_num')    


class SettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Setting
        fields = ('display_style', 'layout_style', 'hot_key')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TagRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagRelation
        fields = ('entry', 'tag')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    setting = serializers.HyperlinkedIdentityField(read_only=True, view_name='setting-detail')
    favorites = FavoriteSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'email', 'password', 'setting', 'favorites')
        extra_kwargs = {'password': {'write_only': True}}


    def validate_username(self, username):
        if not (2 <= len(username) <= 16):
            raise serializers.ValidationError("用户名长度太短")
        return username

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', )

