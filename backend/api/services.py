
from .models import * 
from django.db.models import Prefetch

class UserService():
    @staticmethod
    def get_profile(username):
        try:
            user = User.objects.get(username=username)

            return {'success': True, 'user': user}
        except User.DoesNotExist:
            return {"success": False, "message": f"User with username {username} does not exist"}
    
    @staticmethod
    def follow_user(follower, username, is_follow):
        try:
            followee = User.objects.get(username=username)
            if is_follow:
                followee.followers.add(follower)
            else:
                followee.followers.remove(follower)

            return {'success': True, 'user': followee}
        except User.DoesNotExist:
            return {"success": False, "message": f"User with username {username} does not exist"}

class PostService():
    @staticmethod
    def create_post(user, post):
        post = Post(user=user, post=post)
        post.save()

        return [post, True]

    @staticmethod
    def edit_post(user, post_id, content):
        try:
            post = Post.objects.get(id=post_id)
            if post.user != user:
                return {"success": False, "message": "Authorization denied"}
            else:
                post.post = content
                post.save()

                return {"success": True, "message": "Post successfully updated"}
        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
    
    @staticmethod
    def get_post(post_id):
        try:
            post = Post.objects.get(id=post_id)

            return post
        except Post.DoesNotExist:
            return None
    
    @staticmethod
    def get_like_count(post_id):
        try:
            post = Post.objects.get(id=post_id)
            
            return PostLike.objects.filter(post=post, is_like=True).count()
        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
    
    @staticmethod
    def get_dislike_count(post_id):
        try:
            post = Post.objects.get(id=post_id)
            
            return PostLike.objects.filter(post=post, is_like=False).count()
        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
            
    @staticmethod
    def update_post_like(user, post_id, liked):
        try:
            post = Post.objects.get(id=post_id)

            post_like, created = PostLike.objects.get_or_create(user=user, post=post)
            post_like.is_like=liked
            post_like.save()

            like_count = PostLike.objects.filter(post=post, is_like=True).count()
            dislike_count = PostLike.objects.filter(post=post, is_like=False).count()

            return {"success": True, "message": "Post successfully updated", "like_count": like_count, "dislike_count": dislike_count}

        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
    
    @staticmethod
    def unlike_post(user, post_id):
        try:
            post = Post.objects.get(id=post_id)

            try:
                post_like = PostLike.objects.get(user=user, post=post)
                post_like.delete()

            except PostLike.DoesNotExist:
                pass  

            like_count = PostLike.objects.filter(post=post, is_like=True).count()
            dislike_count = PostLike.objects.filter(post=post, is_like=False).count()

            return {"success": True, "message": "Post successfully updated", "like_count": like_count, "dislike_count": dislike_count}
         

        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}


    @staticmethod
    def is_post_liked(post_id, user):
        try:
            post = Post.objects.get(id=post_id)

            try:
                post_like = PostLike.objects.get(user=user, post=post)
                return post_like.is_like

            except PostLike.DoesNotExist:
                return None           

        except Post.DoesNotExist:
            return {"success": False, "message": "The post does not exist"}
            
    @staticmethod
    def get_all_posts():
        posts = Post.objects.all().order_by('-date_created')
        return posts
    
    @staticmethod
    def get_following_posts(user):
        posts = Post.objects.filter(user__in=user.followees.all())

        return posts
    
    @staticmethod
    def get_user_posts(username):
        try:
            user = User.objects.get(username=username)

            posts = Post.objects.filter(user=user)

            return {"success": True, "posts": posts}

        except User.DoesNotExist:
            return {"success": False, "message": f"User with username {username} does not exist"}

class ChatService():
    @staticmethod
    def get_chats(user):
        chats = Chat.objects.filter(participants=user)
        
        return chats
    
    @staticmethod
    def set_messages_read(chat, user):
        ChatMessage.objects.filter(chat=chat, user=user,read=False).update(read=True)
        
    @staticmethod
    def get_unread_message_count(user):
        return ChatMessage.objects.filter(user=user, recipient=user, read=False).count()

