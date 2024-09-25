from rest_framework import serializers
from movie_app_app.models import CineProfessionls

class EmployeesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    profile = serializers.CharField()
    date_of_birth = serializers.DateField(auto_now_add=True)

    class Meta:
        fields = ['id', 'name', 'profile', 'date_of_birth']
    
    def create(self, validated_data):
        return CineProfessionls.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.profile = validated_data.get("role", instance.profile)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        return instance


class EmployeesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CineProfessionls
        fields = ['id', 'name', 'profile', 'date_of_birth', 'name_length']
        extra_kwargs = {'id': {'read_only': True}, 'name_length': {'read_only': True}}



