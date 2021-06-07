from django.db import models

STATUS_CHOICES = (
    (0, 'задача не выполнена'),
    (1, 'задача не выполнена, отредактирована админом'),
    (10, 'задача выполнена'),
    (11, 'задача отредактирована админом и выполнена'),
)

class User(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=500)
	token = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)

	def __str__(self):
		return "%s %s" % (self.id, self.username)


class Task(models.Model):
	text = models.TextField()
	email = models.EmailField(max_length=100)
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	username = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def to_dict(self):
		return {'id': self.id, 'username' : self.username, 'email': self.email, 'text': self.text, 'status': self.status}

	def __str__(self):
		return "%s %s" % (self.id, self.username)
