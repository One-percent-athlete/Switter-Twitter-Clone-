from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    last_updated = models.DateTimeField(User, auto_now=True)

    profile_img = models.ImageField(null=True, blank=True, upload_to="images/profile_pics/")

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwags):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile,sender=User)

class Swit(models.Model):
    user = models.ForeignKey(User, related_name="swits", on_delete=models.PROTECT)
    body = models.CharField(max_length=250)
    create_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, related_name="swit_like", blank=True)

    def num_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user}"
            f"({self.create_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )