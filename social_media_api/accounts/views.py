from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from notifications.models import Notification
from .serializers import UserSerializer, LoginSerializer,RegisterSerializer
from .models  import CustomUser
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    # get_user_model().objects.create_user
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.create(user=user)
        return Response({'token': token.key})

#profile view for profile management with CustomUser
class ProfileView(generics.GenericAPIView):
    permission_classes  = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self,request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)


#Follow or Unfollow
class FollowView(APIView):
    def post(self,request,pk):
        user_to_follow = CustomUser.objects.get(pk=pk)
        if user_to_follow != request.user:
            if request.user in user_to_follow.user_followers.all():
                user_to_follow.user_followers.remove(request.user)
                request.user.user_following.remove(user_to_follow)
                #send notification
                Notification.objects.create(
                                    recipient=user_to_follow,
                                    actor = request.user,
                                    verb = f"{self.request.user} has Unfollowed you",
                                    target = user_to_follow
                                    )
                return Response({"message": "Unfollowed"}, status=status.HTTP_200_OK)
            else:
                user_to_follow.user_followers.add(request.user)
                request.user.user_following.add(user_to_follow)
                return Response({"message": "Followed"}, status=status.HTTP_201_CREATED)
        return Response({"message":"Cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
