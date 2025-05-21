from urllib import response
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import *  
from .services import *

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer =  self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)

            login(request, user)
            user_serializer = UserAccountSerializer(context={'user': user})
            context = {
                "success": "user account successfully created", 
                "auth": {
                    "user": user_serializer.get_details(),
                    "token": token.key
                }
            }
            return Response(context) 
        else:
            return Response({"errors": serializer.errors})

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = authenticate(self.request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                serializer = self.get_serializer()
                return Response({
                    "auth": {
                        "user": UserAccountSerializer(context={'user': user}).get_details(),
                        "token": token.key
                    }
                })
            else:
                return Response({
                    'errors': {
                        'messages': ['Invalid credentials']
                    }
                })
        else:
            return Response({'errors': serializer.errors})

class LogoutView(generics.RetrieveAPIView):

    def get(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()

            logout(request)

        return Response({'success': 'User logged out successfully'})

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAccountSerializer

    def get(self, request, username):
        serializer = self.get_serializer()
        result = UserService.get_profile(username)

        if result['success']:
            return Response(UserAccountSerializer(context={'user': result['user']}).get_details())
        else:
            return Response({
                'errors': {
                    'messages': [result['message']]
                }
            }) 
class FollowUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def put(self, request, username):
        serializer = FollowSerializer(context={'user': request.user, 'followee': username}, data=request.data)

        if serializer.is_valid():
            result = serializer.follow_user()
            if result['success']:
                data = {
                    'follower': UserAccountSerializer(context={'user': request.user}).get_details(),
                    'followee': UserAccountSerializer(context={'user': result['user']}).get_details()
                }
                return Response(data)
            else:
                return Response({
                    'errors': {
                        'messages': [result['message']]
                    }
                })
        else:
            return Response({'errors': serializer.errors})

class PostRecordsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostService.get_all_posts()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                result = PostService.is_post_liked(item['id'], request.user)
                like_dict = {}
                if (result == True):
                    like_dict['is_liked'] = True
                    like_dict['is_disliked'] = False

                if (result == False):
                    like_dict['is_liked'] = False
                    like_dict['is_disliked'] = True
                
                if (result is None):
                    like_dict['is_liked'] = False
                    like_dict['is_disliked'] = False

                like_dict['like_count'] = PostService.get_like_count(item['id'])
                like_dict['dislike_count'] = PostService.get_dislike_count(item['id'])
                item.update(like_dict)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FollowingPostRecords(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostService.get_all_posts()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = PostService.get_following_posts(request.user)
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                result = PostService.is_post_liked(item['id'], request.user)
                like_dict = {}
                if (result == True):
                    like_dict['is_liked'] = True
                    like_dict['is_disliked'] = False

                if (result == False):
                    like_dict['is_liked'] = False
                    like_dict['is_disliked'] = True
                
                if (result is None):
                    like_dict['is_liked'] = False
                    like_dict['is_disliked'] = False

                like_dict['like_count'] = PostService.get_like_count(item['id'])
                like_dict['dislike_count'] = PostService.get_dislike_count(item['id'])
                item.update(like_dict)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class UserPostRecordsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        un = self.kwargs['username']
        result = PostService.get_user_posts(un)

        return result 

    def list(self, request, username):
        result = self.get_queryset()

        if (result['success']):
            queryset = result['posts']

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                for item in serializer.data:
                    result = PostService.is_post_liked(item['id'], request.user)
                    like_dict = {}
                    if (result == True):
                        like_dict['is_liked'] = True
                        like_dict['is_disliked'] = False

                    if (result == False):
                        like_dict['is_liked'] = False
                        like_dict['is_disliked'] = True
                    
                    if (result is None):
                        like_dict['is_liked'] = False
                        like_dict['is_disliked'] = False

                    like_dict['like_count'] = PostService.get_like_count(item['id'])
                    like_dict['dislike_count'] = PostService.get_dislike_count(item['id'])
                    item.update(like_dict)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({
                'errors': {
                    'messages': [result['message']]
                }
            })

class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            post = serializer.save()

            context = {
                'success': 'Post was successfully created',
                'post': self.serializer_class(post).data
            }

            return Response(context)
        else:
            context = {
                'errors': serializer.errors,
            }

            return Response(context)

class PostEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def put(self, request, post_id):
        serializer = self.serializer_class(data=request.data, context={'user': request.user, 'post_id':post_id})

        if serializer.is_valid():
            result = serializer.edit_post()

            return Response(result)
        else:
            return Response({'errors': serializer.errors})
    
    def get(self, request, post_id):
        post = PostService.get_post(post_id)

        if post is not None:
            return Response(self.serializer_class(post).data)
        else:
            return Response({
                'errors': {
                    'messages': ['Post not found']
                }
            })


class PostUnLikeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUnlikeSerializer

    def put (self, request, post_id):
        serializer = self.serializer_class(data=request.data, context={'user': request.user, 'post_id':post_id})
    
        if serializer.is_valid():
            result = serializer.unlike_post()

            if result['success']:
                return Response(result)
            else:
                return Response({
                    'errors':{
                        'messages': [result.message]
                    }
                })

class PostLikeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeSerializer

    def put (self, request, post_id):
        serializer = self.serializer_class(data=request.data, context={'user': request.user, 'post_id':post_id})
    
        if serializer.is_valid():
            result = serializer.update_post_like()

            return Response(result)

class ChatRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        return ChatService().get_chats(self.request.user)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request':request})
        data = serializer.data

        return Response({
            'chats':data,
            'unread_count': ChatService.get_unread_message_count(request.user)
        })

class MessagesStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
            ChatService.set_messages_read(chat, request.user)
            
            return Response({
                'message': 'messages successfully updated'
            })
        except Chat.DoesNotExist:
            return Response({
                    'errors':{
                        'messages': ['Chat does not exist']
                    }
                })

def index(request):
    return render(request, "index.html")

        
