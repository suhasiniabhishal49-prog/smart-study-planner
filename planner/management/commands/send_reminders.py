from django.core.management.base import BaseCommand
from django.utils import timezone
from planner.models import Task


class Command(BaseCommand):
    help = 'Check and send reminders for due tasks'

    def handle(self, *args, **options):
        now = timezone.now()
        pending_reminders = Task.objects.filter(
            reminder_time__lte=now,
            reminder_sent=False
        ).select_related('user', 'subject')

        if not pending_reminders.exists():
            self.stdout.write(self.style.SUCCESS('No pending reminders found.'))
            return

        sent_count = 0
        for task in pending_reminders:
            if task.status == 'Pending':
                status_text = "PENDING — complete it soon!"
            else:
                status_text = "COMPLETED — nice work!"

            message = (
                f"🚨 REMINDER: '{task.title}' "
                f"(Subject: {task.subject.name}, User: {task.user.username}) "
                f"Status: {task.status}. {status_text} "
                f"Reminder: {task.reminder_time}, Deadline: {task.deadline}"
            )
            print(message)
            self.stdout.write(message)
            
            task.reminder_sent = True
            task.save(update_fields=['reminder_sent'])
            sent_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {sent_count} reminders.')
        )
