from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def save(self,*args,**kwargs):
        self.slug=slugify(self.body, allow_unicode=True)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id, self.slug))

    def likes_count(self):
        return self.post_likes.count()

    def user_can_like(self, user):
        user_like = user.user_likes.filter(post=self)
        if user_like.exists():
            return True
        return False



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replay_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.body[:30]}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self) -> str:
        return f'{self.user} liked {self.post.slug}'
    