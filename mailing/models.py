from django.db import models
import django as django
from django.template.defaultfilters import slugify as d_slugify
from config import settings
from django.utils import timezone

NULLABLE = {'blank': True, "null": True}

def slugify(words: str) -> str:
    """
    Slugify for russian language.
    """
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                'ю': 'yu',
                'я': 'ya'}

    return d_slugify(''.join(alphabet.get(w, w) for w in words.lower()))
class Client(models.Model):
    """Model of client for sending"""
    full_name = models.CharField(max_length=300, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='email')
    description = models.TextField(max_length=600, **NULLABLE, verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, null=False, verbose_name='URL')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        """Return client mail for fast sending"""
        return self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class Transfer(models.Model):
    """Model transfer for sending"""
    class TransferStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'
        Running = 'READY'
        Finished_error = 'FINISHED_WITH_ERROR'

    class TransferPeriodicity(models.TextChoices):
        Daily = 'DAILY'
        Weekly = 'WEEKLY'
        Monthly = 'MONTHLY'

    title = models.CharField(max_length=100, verbose_name="transfer name", unique=True)
    time = models.TimeField(verbose_name="start time for send", default=django.utils.timezone.now)
    periodicity = models.CharField(choices=TransferPeriodicity.choices)
    status = models.CharField(choices=TransferStatus.choices, default=TransferStatus.Created)
    message = models.ForeignKey("Messages", on_delete=models.SET_NULL, **NULLABLE)
    client = models.ManyToManyField("Client")
    slug = models.SlugField(max_length=255, verbose_name="transmission slug", null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        """Save slug to transfer base"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer: {self.title}"

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"

    def get_statistic(self):
        """Get statistic of send. Use Related name in Statistic"""
        return self.logs_of_transfers.all()

    def get_messages(self):
        """Get message for transmission when used scheduler"""
        messages = self.message
        return messages

    def get_clients(self):
        """Get clients for transmission when used scheduler"""
        clients = self.client.all()
        return clients

class Messages(models.Model):
    """Model message for clients for sending"""
    topic = models.CharField(max_length=50, verbose_name="message topic", null=False, blank=False, unique=True)
    body = models.TextField(max_length=500, verbose_name="message body", null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=255, verbose_name="message slug", null=False, unique=True)


    def __str__(self):
        return self.topic


    def save(self, *args, **kwargs):
        """Save slug to message base"""
        if not self.slug:
            self.slug = slugify(self.topic)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

class Logs(models.Model):
    """Model for statistic of transmissions"""

    class AttemptStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'

    transfer = models.ForeignKey("Transfer", on_delete=models.CASCADE, related_name="logs_of_transfers")
    time = models.DateTimeField(verbose_name="last time for send", default=None, null=True, blank=True)
    status = models.CharField(choices=AttemptStatus.choices, default=AttemptStatus.Created)
    mail_answer = models.CharField(verbose_name="answer from mailserver", default=None, null=True, blank=True)


    def __str__(self):
        return f"Status: {self.status} Time: {self.time} Mail answer: {self.mail_answer}"


    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"