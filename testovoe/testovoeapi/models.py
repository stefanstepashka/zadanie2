from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    uploaded_file = models.CharField(max_length=200, unique=True)
    file_content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class SelectedMethod(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, related_name='selected_methods', on_delete=models.CASCADE)
    method_type = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.method_type} {self.path}"




from django.db import models

# Create your models here.
