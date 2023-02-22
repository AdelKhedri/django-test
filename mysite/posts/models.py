from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=100, verbose_name="title")
    poster = models.ImageField(upload_to='posts/poster_images/', verbose_name="Poster")
    content = models.CharField(max_length=2000, verbose_name="Content")
    publish_time = models.DateTimeField()
    active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    auther = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Auther")
    views = models.IntegerField()
    likes = models.ManyToManyField(User)

    def get_posts(self):
        if self.is_deleted == False and self.active and self.publish_time < timezone.now():
            return True
            
    def __str__(self):
        return self.title

class Video(models.Model):
    titel = models.CharField(max_length=150, verbose_name="Titel")
    content = models.CharField(max_length=500, verbose_name='Content')
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Auther_video")
    is_active = models.BooleanField(default=False, verbose_name="Active")
    is_deleted = models.BooleanField(default=False, verbose_name="delete")
    likes = models.ManyToManyField(User, verbose_name="Likes")
    views = models.IntegerField(default=0, verbose_name="Views")

    def __str__(self):
        return self.titel


class MoreVideoPost(models.Model):
    post_1 = models.ForeignKey(Post, related_name="post1", on_delete=models.CASCADE)
    post_2 = models.ForeignKey(Post, related_name="post2", on_delete=models.CASCADE)
    video_1 = models.ForeignKey(Video, related_name="video1", on_delete=models.CASCADE)
    video_2 = models.ForeignKey(Video, related_name="video2", on_delete=models.CASCADE)

    def __str__(self):
        return self.post_1.title

class Comment(models.Model):
    text = models.CharField(max_length=200, verbose_name="text")
    parent_id = models.IntegerField(verbose_name="parent id fiel")
    parent_id_user = models.IntegerField(verbose_name="parent id user")
    type_model = models.CharField(max_length=10)
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Auhter_comment")

    def __str__(self):
        return self.text

class otp_user(models.Model):
    random_code= models.IntegerField()
    time_code = models.DateTimeField()
    phone = models.CharField(max_length=11)
    user = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.phone