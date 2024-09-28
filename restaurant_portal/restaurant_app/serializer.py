from rest_framework import serializers
from restaurant_app.models import Employees, Restaurant, RestaurantReview
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize

class EmployeesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    role = serializers.CharField()
    qualification = serializers.CharField()

    class Meta:
        fields = ['id', 'name', 'role', 'qualification']
    
    def create(self, validated_data):
        return Employees.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.role = validated_data.get("role", instance.role)
        instance.qualification = validated_data.get("qualification", instance.qualification)
        return instance


class EmployeesModelSerializer(serializers.ModelSerializer):

    role_fuzz = serializers.SerializerMethodField()
    wordtoken = serializers.SerializerMethodField()

    class Meta:
        model = Employees
        fields = ['id', 'name', 'role', 'qualification', 'name_length', 'role_fuzz', 'wordtoken']
        extra_kwargs = {'id': {'read_only': True}, 'name_length': {'read_only': True}}

    def get_role_fuzz(self, obj):
        return fuzz.ratio(obj.qualification, 'MBA')
    
    def get_wordtoken(self, obj):
        return word_tokenize(obj.qualification)
    
    def to_internal_value(self, data):
        # data['name'] = data['name'] + ' Kumar'
        return super().to_internal_value(data)

    def run_validation(self, data):
        return super().run_validation(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['name'] == "Sheela Kumar":
            ret['name'] = 'Sheela Godwin'
        return ret


class RestaurantReviewModelSerializer(serializers.ModelSerializer):

    managerName = serializers.CharField(source="restaurantName.manager.name", required=False, read_only=True)
    reviewLength = serializers.IntegerField(source='review_length', required=False, read_only=True)
    
    class Meta:
        model = RestaurantReview
        fields = ['id', 'restaurantName', 'review', 'managerName', 'reviewLength']
        extra_kwargs = {'id': {'read_only': True}}
    
    

class RestaurantModelSerializer(serializers.ModelSerializer):

    restaurantReview = RestaurantReviewModelSerializer(source="restaurant_review", many=True, required=False, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant', 'restaurantType', 'location', 'waiters', 'manager', 'chefName', 'restaurantReview']
        extra_kwargs = {'id': {'read_only': True}}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['restaurant'] = ret['restaurant'] + ' Kumar'
        return ret

class combinedModelSerializer(serializers.ModelSerializer):

    restaurant = RestaurantModelSerializer(source="restaurant_Manager", many=True)

    class Meta:
        model = Employees
        fields = '__all__'