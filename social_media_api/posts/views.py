from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticatedOrReadOnly
from .models import Comment, Post
from posts.serializers import PostSerializer, CommentSerializer

#Post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self,request,pk):
        post = Post.objects.get(pk=pk)
        content = request.data.get('content')
    #create comment
        comment = Comment.objects.create(
            user = request.user,
            post=post,
            content=content
        )
        return Response({'message':'comment added'},status=status.HTTP_200_OK)
    
    