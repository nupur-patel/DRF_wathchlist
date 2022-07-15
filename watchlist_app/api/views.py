# from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from watchlist_app.api.serializers import *
from watchlist_app.models import *
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.throttling import *
from watchlist_app.api.pagination import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, mixins, viewsets, status, filters
from rest_framework.permissions import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import LimitOffsetPagination


class UserReview(generics.ListAPIView):
	serializer_class = ReviewSerializer

	# def get_queryset(self):
	# 	usernmae = self.kwargs['username']
	# 	return Review.objects.filter(review_user__username = usernmae)

	def get_queryset(self):
		username = self.request.query_params.get('username', None)
		return Review.objects.filter(review_user__username = username)



class ReviewCreate(generics.CreateAPIView):   
	permission_classes = [IsAuthenticated]
	serializer_class = ReviewSerializer
	throttle_classes = [ReviewCreateThrottle]

	def get_queryset(self):
		return Review.objects.all()

	# overwriting method
	def perform_create(self, serializer):
		pk = self.kwargs.get('pk')
		watchlist = WatchList.objects.get(pk=pk)

		review_user = self.request.user
		review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)

		if review_queryset.exists():
			raise ValidationError("You have already reviewed this movie")

		if watchlist.number_rating == 0:
			watchlist.avg_rating = serializer.validated_data['rating']
		else:
			watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

		watchlist.number_rating = watchlist.number_rating + 1
		watchlist.save()

		serializer.save(watchlist = watchlist, review_user = review_user)

class ReviewList(generics.ListAPIView):
	# queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	# permission_classes = [IsAuthenticated]
	# throttle_classes = [ReviewListThrottle, AnonRateThrottle]

	# filter_backends = [DjangoFilterBackend]
	# filterset_fields = ['review_user__username', 'active']

	# filter_backends = [filters.SearchFilter]
	# search_fields = ['watchlist__title','review_user__username']

	filter_backends = [filters.OrderingFilter]
	ordering_fields = ['review_user__username']

	# overwriting method
	def get_queryset(self):
		pk = self.kwargs['pk']
		return Review.objects.filter(watchlist = pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer  
	permission_classes = [IsReviewUserOrReadOnly]
	throttle_classes = [ScopedRateThrottle]
	throttle_scope = 'review-detail'
	

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
# 	queryset = Review.objects.all()
# 	serializer_class = ReviewSerializer

# 	def get(self, request, *args, **kwargs):
# 		return self.list(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
# 		return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
# 	queryset = Review.objects.all()
# 	serializer_class = ReviewSerializer

# 	def get(self, request, *args, **kwargs):
# 		return self.retrieve(request, *args, **kwargs)
class WatchListTemp(generics.ListAPIView):
	queryset = WatchList.objects.all()
	serializer_class = WatchListSerializer
	# pagination_class = WatchListPagination
	pagination_class = WatchListCPagination
	


	# filter_backends = [filters.OrderingFilter]
	# ordering_fields = ['avg_rating']

class WatchListAV(APIView):
	permission_classes = [IsAdminOrReadOnly]

	def get(self, request):
		paginator = LimitOffsetPagination()
		movies = WatchList.objects.all()
		result_page = paginator.paginate_queryset(movies, request)
		serializer = WatchListSerializer(result_page, many=True )
		return Response(serializer.data)

	def post(self, request):
		serializer = WatchListSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)


class WatchListDetailAV(APIView):
	permission_classes = [IsAdminOrReadOnly]

	def get(self, request, pk):
		try:
			movies = WatchList.objects.get(pk = pk)
		except Movie.DoesNotExist:
			return Response({'Error': "Movie Not Found"}, status = status.HTTP_404_NOT_FOUND)

		serializer = WatchListSerializer(movies)
		return Response(serializer.data)

	def put(self,request,pk):
		movies = WatchList.objects.get(pk = pk)
		serializer = WatchListSerializer(movies, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		movie = WatchList.objects.get(pk=pk)
		movie.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

class StreamPlatformAV(APIView):
	permission_classes = [IsAdminOrReadOnly]
	def get(self, request):
		obj = StreamPlatform.objects.all()
		serializer = StreamPlatformSerializer(obj, many=True, context={'request': request})
		return Response(serializer.data)

	def post(self, request):
		serializer = StreamPlatformSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)


# class StreamPlatformVS(viewsets.ViewSet):
# 	def list(self, request):
# 		obj = StreamPlatform.objects.all()
# 		serializer = StreamPlatformSerializer(obj, many=True)
# 		return Response(serializer.data)

# 	def retrieve(self, request, pk = None):
# 		obj = StreamPlatform.objects.all()
# 		watchlist = get_object_or_404(obj, pk=pk)
# 		serializer = StreamPlatformSerializer(watchlist)
# 		return Response(serializer.data)

# 	def create(self, request):
# 		serializer = StreamPlatformSerializer(data = request.data)
# 		print("I am here")
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			print("Here2")
# 			return Response(serializer.errors)

class StreamPlatformVS(viewsets.ModelViewSet):
	permission_classes = [IsAdminOrReadOnly]
	queryset = StreamPlatform.objects.all()
	serializer_class = StreamPlatformSerializer

class StreamPlatformDetailAV(APIView):
	permission_classes = [IsAdminOrReadOnly]
	def get(self,request,id):
		try:
			obj = StreamPlatform.objects.get(id = id)
		except StreamPlatform.DoesNotExist:
			return Response({'Error': "Streaming platform Not Found"}, status = status.HTTP_404_NOT_FOUND)

		serializer = StreamPlatformSerializer(obj)
		return Response(serializer.data)

	def put(self,request,id):
		movies = StreamPlatform.objects.get(id = id)
		serializer = StreamPlatformSerializer(movies, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id):
		movie = StreamPlatform.objects.get(id=id)
		movie.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

# @api_view(['GET','POST'])
# def movie_list(request):
# 	if request.method == 'GET':
# 		movies = WatchList.objects.all()
# 		serializer = WatchListSerializer(movies, many=True)
# 		return Response(serializer.data)
		
# 	if request.method == 'POST':
# 		serializer = WatchListSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			return Response(serializer.errors)



# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
# 	if request.method == 'GET':
# 		try:
# 			movies = WatchList.objects.get(pk = pk)
# 		except Movie.DoesNotExist:
# 			return Response({'Error': "Movie Not Found"}, status = status.HTTP_404_NOT_FOUND)
# 		serializer = WatchListSerializer(movies)
# 		return Response(serializer.data)

# 	if request.method == 'PUT':
# 		movies = WatchList.objects.get(pk = pk)
# 		serializer = WatchListSerializer(movies, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# 	if request.method == 'DELETE':
# 		movie = WatchList.objects.get(pk=pk)
# 		movie.delete()
# 		return Response(status = status.HTTP_204_NO_CONTENT)


