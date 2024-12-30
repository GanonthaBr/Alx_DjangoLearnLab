from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from .models import Comment, Post, Like
from posts.serializers import PostSerializer, CommentSerializer
from .pagination import PostPagination, CommentPagination
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import generics
from notifications.models import Notification


#Post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [SearchFilter]
    search_fields = ['title','content'],

    def post(self,request):
        content = request.data.get('content')
        title = request.data.get('title')
    #create post
        post = Post.objects.create(
            content=content,
            title=title,
            author=request.user,
        )
        return Response({'message':'Post created!'},status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommentPagination

    def post(self,request,pk):
        post = Post.objects.get(pk=pk)
        content = request.data.get('content')
    #create comment
        comment = Comment.objects.create(
            author = self.request.user,
            post=post,
            content=content
        )
        return Response({'message':'comment added'},status=status.HTTP_200_OK)
    

#Personalized Feed
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        following_users = request.user.following.all().values_list('id', flat=True)
        if not following_users:
            return Response({"message": "No posts available"}, status=status.HTTP_200_OK)
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serialized_data = PostSerializer(posts, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    

#Like
class LikeView(APIView):
    def post(self,request,pk):
        post = generics.get_object_or_404(Post,pk=pk)
        like, created = Like.objects.get_or_create(user=request.user,post=post)
        if created:
            return Response({"message":"Post  Liked"},status=status.HTTP_201_CREATED)
        else:
            user_recipient = post.author
            Notification.objects.create(
                                    recipient=user_recipient,
                                    actor = request.user,
                                    verb = 'Unliked your post',
                                    target = post
                                    )
            like = Like.objects.filter(user=request.user, post=post)
            like.delete()    
            return Response({"message":"Post unliked"}, status=status.HTTP_200_OK)