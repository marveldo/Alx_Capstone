from rest_framework import serializers
from .models import BlogPost,CustomUser, Tag , Category


class TagSerializer(serializers.ModelSerializer):
    """A serializer for the Tag Model
    """
    class Meta :
        model = Tag 
        fields = ['tag_name']

class CategorySerializer(serializers.ModelSerializer):
    """A serializer from the Category Model
    """
    class Meta :
        model = Category
        fields = ['category_name']

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the User Model
    """
    class Meta :
        model = CustomUser
        fields = ['id','username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only' : True , 'required' : False}, "*": {'required': False}}

    def validate(self, attrs):
        if not self.instance and not attrs.get('username'):
            raise serializers.ValidationError({'username': 'Username may not be blank'})
        if not self.instance and not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Email may not be blank'})        
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Password may not be blank'})
        
        return super().validate(attrs)
        


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data : dict):
        password = validated_data.pop('password', None)

        for name, value in validated_data.items() :
            setattr(instance , name , value )
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance

class BlogPostSerializer(serializers.ModelSerializer):
    """ Serializer for the Blog Model
    """
    tags = serializers.CharField(max_length = 120, write_only=True)
    categories = serializers.CharField(max_length = 120, write_only=True)

    tag_field = serializers.SerializerMethodField()

    category_field = serializers.SerializerMethodField()
    class Meta :
        model = BlogPost
        exclude = ['user']

    def get_tag_field(self , obj):
        """Method that handles the Tag Field Method serializer
        """
        tags = obj.tags.all()
        serializer = TagSerializer(tags, many=True)
        return serializer.data
    
    def get_category_field(self, obj):
        """Method that handles the Category Field Method Serializer
        """
        categories = obj.categories.all()
        serializer = CategorySerializer(categories, many=True)
        return serializer.data

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags', None)
        categories = validated_data.pop('categories', None)

        blog = BlogPost.objects.create(user=request.user , **validated_data)
        if tags is not None :
            tag , created = Tag.objects.get_or_create(tag_name = tags)
            blog.tags.add(tag)
        
        if categories is not None :
            category , created = Category.objects.get_or_create(category_name = categories)
            blog.categories.add(category)
        

        blog.save()
        return blog
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        categories = validated_data.pop('categories', None)

        for name , value in validated_data.items():
            setattr(instance, name, value)

        if tags is not None :
            tag , created = Tag.objects.get_or_create(tag_name = tags)
            instance.tags.add(tag)
        
        if categories is not None :
            category , created = Category.objects.get_or_create(category_name = categories)
            instance.categories.add(category)

        instance.save() 
        return instance
