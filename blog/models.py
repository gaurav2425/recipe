from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from tinymce.models import HTMLField  
  
  
class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255,unique = True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)     #, null=True)
    slug=models.CharField(max_length=130)
    views= models.IntegerField(default=0)
    timeStamp=models.DateTimeField(default = now)
    content =  HTMLField() 


    def __str__(self):
        return self.title + " by " + self.author.username

    def get_absolute_url(self):
        return reverse("blog:blogPost", kwargs={"slug": self.title})
    

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
    

# from django.contrib.auth.models import User
class PostViews(models.Model):
    IPAddres= models.GenericIPAddressField(default="45.243.82.169")
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} in {1} post'.format(self.IPAddres,self.post.title)