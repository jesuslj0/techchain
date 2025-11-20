# posts/serializers.py

from rest_framework import serializers
from .models import Post, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostCreateSerializer(serializers.ModelSerializer):
    # Los tags se manejarán por sus IDs durante la creación.
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'content', 'tags', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def validate_tags(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Un post no puede tener más de 5 tags.")
        return value

# Serializador para listar/detallar posts (incluye el nombre de usuario)
class PostListSerializer(PostCreateSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True) 

    class Meta(PostCreateSerializer.Meta):
        model = Post
        fields = PostCreateSerializer.Meta.fields + ['username']
        read_only_fields = fields