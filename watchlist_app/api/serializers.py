from rest_framework import serializers
from watchlist_app.models import *

class ReviewSerializer(serializers.ModelSerializer):
	review_user = serializers.StringRelatedField(read_only = True)
	class Meta:
		model = Review
		exclude = ('watchlist',)
		# fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
	# name_len = serializers.SerializerMethodField()
	# review = ReviewSerializer(many = True, read_only = True)
	platform = serializers.CharField(source='platform.name')

	class Meta:
		model = WatchList
		fields = '__all__'
		# fields = ['id', 'name', 'description']
		# exclude = ['active']

	# def get_name_len(self, obj):
	# 	length = len(obj.name)
	# 	return length

class StreamPlatformSerializer(serializers.ModelSerializer):

	# watchlist = WatchListSerializer(many = True, read_only = True)
	# review_user = serializers.StringRelatedField(read_only = True,many = True)
	watchlist = WatchListSerializer(many = True,read_only = True)
	# watchlist = serializers.HyperlinkedRelatedField(many = True, read_only = True, view_name = "movie-detail")

	class Meta:
		model = StreamPlatform
		fields = '__all__'	


# def name_length(value):
# 	if len(value) < 2:
# 		raise serializers.ValidationError("name is too short!")
# 	return value

# class WatchListSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only = True)
# 	name = serializers.CharField(validators = [name_length])
# 	description = serializers.CharField()
# 	active = serializers.BooleanField()

# 	def create(self, validated_data):
# 		return WatchList.objects.create(**validated_data)

# 	def update(self, instance, validated_data):
# 		instance.name = validated_data.get('name', instance.name)
# 		instance.description = validated_data.get('description', instance.description)
# 		instance.active = validated_data.get('active', instance.active)
# 		instance.save()
# 		return instance

	# def validate_name(self,value):
	# 	if len(value) < 2:
	# 		raise serializers.ValidationError("name is too short!")
	# 	else:
	# 		return value

	# def validate(self,data):
	# 	if data['name'] == data['description']:
	# 		raise serializers.ValidationError("Two field should not be same")
	# 	return data







