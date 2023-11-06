from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	likes = models.ManyToManyField(User, related_name="post_like")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})
	def number_of_likes(self):
		return self.likes.count()

#Comments
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    name = models.CharField(max_length = 25)
    content = models.CharField(max_length = 220)
    date_commented = models.DateTimeField( auto_now_add=True)
	
    class Meta:
        ordering = ['-date_commented']
    """
    def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
    """