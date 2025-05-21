from rest_framework import serializers
from django.contrib.auth import authenticate, login
from .models import * 
from .services import *


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        read_only_fields = ['username', 'email']
        depth = 1
    
    def get_details(self):
        user = self.context['user']

        return {
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.strftime("%b.%d.%Y, %H:%M %p"),
            'followees': [followee.username for followee in user.followees.all()],
            'followers': [follower.username for follower in user.followers.all()]
        }
    
class FollowSerializer(serializers.Serializer):
    follow = serializers.BooleanField()

    def follow_user(self):
        follower = self.context['user']
        followee = self.context['followee']

        result = UserService.follow_user(follower, followee, self.validated_data['follow'])

        return result

class PostSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer(read_only=True)
    date_created = serializers.DateTimeField(format="%b.%d.%Y, %H:%M %p", read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['date_created']
        depth = 1
    
    def save(self):
        post, created = PostService.create_post(user=self.context['user'], post=self.validated_data['post'])
        return post
    
    def edit_post(self):
        result = PostService.edit_post(user=self.context['user'], post_id=self.context['post_id'], content=self.validated_data['post'])
        
        return result

class PostUnlikeSerializer(serializers.ModelSerializer):
    unlike = serializers.BooleanField()

    class Meta:
        model = PostLike
        fields = ['unlike']
    
    def unlike_post(self):
        result = PostService.unlike_post(user=self.context['user'], post_id=self.context['post_id'])

        return result

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['is_like']
 
    def update_post_like(self):
        result = PostService.update_post_like(user=self.context['user'], post_id=self.context['post_id'], liked=self.validated_data['is_like'])

        return result
class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")
    recipient = serializers.ReadOnlyField(source="recipient.username")
    incoming = serializers.SerializerMethodField(method_name="is_incoming")
    timestamp = serializers.DateTimeField(format="%b %d %Y, %I:%M %p")
    
    class Meta:
        model = ChatMessage
        exclude = ('user','chat',)
        depth = 1
    
    def is_incoming(self, message):
        incoming = True
        if self.context['user'] == message.sender:
            incoming = False
        
        return incoming
    
class ChatSerializer(serializers.ModelSerializer):
    chat_messages = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    participants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    last_activity = serializers.DateTimeField(format="%b %d %Y, %I:%M %p")

    class Meta:
        model = Chat
        fields = ['id','participants','last_activity', 'chat_messages', 'unread_count']
        depth = 1
    
    def get(self):
        return {
            'id': self.id,
            'last_activity': self.last_activity.strftime("%b %d %Y, %I:%M %p"),
            'participants': [{'id': participant.id, 'username': participant.username} for participant in self.participants.all()],
            'messages': [message.serialize() for message in self.chat_messages.filter(user=self.context['user']).all()]
        }
        
    def get_chat_messages(self, chat):
        messages = chat.chat_messages.filter(user=self.context['request'].user)
        serializer = ChatMessageSerializer(messages, many=True, context={'user':self.context['request'].user})
        
        return serializer.data

    def  get_unread_count(self, chat):
        return chat.chat_messages.filter(user=self.context['request'].user,recipient=self.context['request'].user, read=False).count()

    