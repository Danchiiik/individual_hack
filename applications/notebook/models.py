from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


# def sup_user():
#     return User.objects.get(email='admin@gmail.com')

class Notebook(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/')
    
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Notebooks'
        verbose_name = 'Notebook'
        
    
class Image(models.Model):
    notebook_obj = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    
    def __str__(self) -> str:
        return str(self.image)
        
        
        

class Like(models.Model):
    like = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    notebook_obj = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='likes')
    
    def __str__(self) -> str:
        return self.like


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    notebook_obj = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(
        validators= [
        MinValueValidator(1),
        MaxValueValidator(10)
        ], blank=True, null= True
    )
    
    def __str__(self) -> str:
        return self.rating
    
    
class Comment(models.Model):
    notebook_obj = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='comments',)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.owner.email
    

    
    
    
class Favourite(models.Model):
    notebook_obj = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='favourites')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.owner} -  {self.favourite}'
    
    
class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    notebook_obj = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='orders')
    amount = models.PositiveIntegerField(default=1)
    order = models.BooleanField(default=False)
    order_code = models.CharField(max_length=100, blank=True)
    
    def __str__(self) -> str:
        return f'{self.owner} - {self.notebook_obj}'
    
    
    def create_order_code(self):
        import uuid
        self.order_code = str(uuid.uuid4())
    
    
        