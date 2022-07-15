from django.urls import path, include
from watchlist_app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream',views.StreamPlatformVS, basename = 'streamplatform')

urlpatterns = [
	path('list/',views.WatchListAV.as_view(), name = "movie-list" ),
	path('list2/',views.WatchListTemp.as_view(), name = "movie-list2" ),
	path('<int:pk>', views.WatchListDetailAV.as_view(), name = "movie-detail"),

	# path('stream/', StreamPlatformAV.as_view(), name = 'stream-platform'),
	# path('stream/<int:id>', StreamPlatformDetailAV.as_view(), name="stream-detail"),

	path('<int:pk>/reviews/',views.ReviewList.as_view(), name = "review-list"),
	path('<int:pk>/review-create/',views.ReviewCreate.as_view(), name = "review-create"),
	path('review/<int:pk>', views.ReviewDetail.as_view(), name = "review-detail"),

	path('',include(router.urls)),
	path('review/', views.UserReview.as_view(), name = 'user-review-detail')
	
	# path('review/', ReviewList.as_view(), name = "review-list"),
	# path('review/<int:pk>', ReviewDetail.as_view(), name="review-detail"),
]



