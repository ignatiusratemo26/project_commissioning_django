from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail  # For email notifications
from django.conf import settings
from .models import Project, Notification

@receiver(post_save, sender=Project)
def notify_user_on_approval(sender, instance, **kwargs):
    user = instance.created_by
    notifications = []
    
    if instance.approved_for_commissioning:
        message = f"Your project '{instance.name}' has been approved for commissioning."
        notifications.append(message)

    if instance.approved_for_occupancy:
        message = f"Your project '{instance.name}' has been approved for occupancy."
        notifications.append(message)
    
    if notifications:
        # Create notifications in the database
        for message in notifications:
            Notification.objects.create(user=user, project=instance, message=message)

        # Send an email notification (optional)
        send_mail(
            subject="Project Approval Notification",
            message="\n".join(notifications),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
