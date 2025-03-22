from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WorkersActivity(models.Model):
    """
    Model to track actions performed by workers on the platform.
    
    Attributes:
        worker (ForeignKey): Links to the User model, representing the worker who performed the action.
        workersAction (CharField): Describes the specific action performed by the worker.
        created_at (DateTimeField): Stores the timestamp when the action was recorded.
    """
    
    worker = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Deletes worker activity if the user is deleted
        help_text="The worker responsible for this activity."
    )
    workersAction = models.CharField(
        max_length=150, 
        verbose_name="Worker's Actions", 
        help_text="Description of the worker's action."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically set to the current timestamp when created
        help_text="The date and time when this activity was recorded."
    )

    class Meta:
        verbose_name = "Worker's Activity"  # Name displayed in Django Admin
        verbose_name_plural = "Worker's Activities"  # Plural name in Django Admin
        ordering = ['-created_at']  # Sort activities in descending order (latest first)
    
    def __str__(self):
        """Returns a human-readable representation of the worker's activity."""
        return f"{self.worker.username} - {self.workersAction} ({self.created_at})"
