from django.db import models
import uuid
from users.models import Profile
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Projects(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True, default="project_images/default.jpg", upload_to='project_images')
    tags = models.ManyToManyField(Tag, blank=True)
    total_votes = models.IntegerField(default=0, null=True, blank=True)
    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    demo_link = models.CharField(max_length=500, null=True, blank=True) # todo check blank
    source_link = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)

    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner_id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes/totalVotes) * 100
        self.votes_ratio = totalVotes
        self.votes_ratio = ratio
        self.save()


class Review(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    review_text = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False)

    def __str__(self):
        return self.value


