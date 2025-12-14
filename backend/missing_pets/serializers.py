from rest_framework import serializers
from .models import MissingPet, MissingPetImage
from users.serializers import UserSerializer


class MissingPetImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MissingPetImage
        fields = ('id', 'image', 'is_primary', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class MissingPetListSerializer(serializers.ModelSerializer):
    
    reporter_name = serializers.CharField(source='reporter.full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = MissingPet
        fields = (
            'id', 'name', 'category', 'category_display', 'breed',
            'gender', 'last_seen_location', 'last_seen_date',
            'reward_offered', 'status', 'primary_image',
            'reporter_name', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            return request.build_absolute_uri(primary.image.url) if request else primary.image.url
        return None


class MissingPetDetailSerializer(serializers.ModelSerializer):
    
    reporter = UserSerializer(read_only=True)
    images = MissingPetImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MissingPet
        fields = (
            'id', 'reporter', 'name', 'category', 'category_display',
            'breed', 'gender', 'gender_display', 'description',
            'last_seen_location', 'last_seen_date', 'reward_offered',
            'contact_phone', 'contact_email', 'status', 'status_display',
            'is_active', 'images', 'created_at', 'updated_at', 'found_date'
        )
        read_only_fields = ('id', 'reporter', 'created_at', 'updated_at', 'found_date')


class MissingPetCreateUpdateSerializer(serializers.ModelSerializer):
    
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True,
        max_length=5
    )
    
    class Meta:
        model = MissingPet
        fields = (
            'name', 'category', 'breed', 'gender', 'description',
            'last_seen_location', 'last_seen_date', 'reward_offered',
            'contact_phone', 'contact_email', 'images'
        )
    
    def validate_last_seen_date(self, value):
       
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Last seen date cannot be in the future.")
        return value
    
    def validate_reward_offered(self, value):
       
        if value is not None and value < 0:
            raise serializers.ValidationError("Reward cannot be negative.")
        return value
    
    def validate_images(self, value):
    
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 images allowed.")
        
        for image in value:
            if image.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image size must be less than 5MB.")
        
        return value
    
    def create(self, validated_data):
        #Create missing pet report with images
        images_data = validated_data.pop('images', [])
        missing_pet = MissingPet.objects.create(**validated_data)
        
        for index, image in enumerate(images_data):
            MissingPetImage.objects.create(
                missing_pet=missing_pet,
                image=image,
                is_primary=(index == 0)
            )
        
        return missing_pet
    
    def update(self, instance, validated_data):
        validated_data.pop('images', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance