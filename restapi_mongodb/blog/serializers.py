from rest_framework import serializers

from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        
        # model for serializer
        model = Blog

        #  a tuple of field names to be included in the serialization
        fields = (
            'id',
            'title',
            'description',
            'published'
        )