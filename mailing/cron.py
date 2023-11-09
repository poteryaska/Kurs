import smtplib

import time
import schedule
from datetime import datetime, timedelta
import mailing.models

import mailing.models
from django.core.mail import send_mail
from django.conf import settings


def sendmails(transfer_id: str, emails_base: list, message_topic: str, message_body: str) -> None:
    try:
        send_mail(message_topic, message_body, settings.EMAIL_HOST_USER, emails_base, fail_silently=True)

        statistic = mailing.models.Logs.objects.get(transfer_id=transfer_id)
        statistic.status = "FINISHED"
        statistic.mail_answer = "OK"
        statistic.time = datetime.now()
        statistic.save()

        change_transfer_status = mailing.models.Transfer.objects.get(id=transfer_id)
        change_transfer_status.status = "FINISHED"
        change_transfer_status.save()
        print("SEND MAIL")

    except smtplib.SMTPException as error:

        print("PROBLEMS WITH SEND MAIL")
        statistic = mailing.models.Logs.objects.get(transfer_id=transfer_id)
        statistic.status = "FINISHED"
        statistic.mail_answer = "ERROR"
        statistic.time = datetime.now()
        statistic.save()

        change_transfer_status = mailing.models.Transfer.objects.get(id=transfer_id)
        change_transfer_status.status = "FINISHED_WITH_ERROR"
        change_transfer_status.save()


def run_transfer():

    schedule.clear()
    active_transfer = mailing.models.Transfer.objects.filter(is_published=True)
    print("PREPARE SEND")

    for transfer in active_transfer:
        emails_base = []
        print("TRANSFER TITLE:", transfer.title)

        if transfer.periodicity == "DAILY":
            print("TYPE: SEND DAILY")
            print("ID:", transfer.pk)
            convert_time = str(transfer.time)[:5]
            print("TIME:", convert_time)
            message = transfer.get_messages()
            print("MESSAGE TOPIC:", message.topic)
            print("MESSAGE BODY:", message.body)
            for client_mail in transfer.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)

                schedule.every().day.at(convert_time).do(sendmails,
                                                         emails_base=emails_base,
                                                         message_topic=message.topic,
                                                         message_body=message.body,
                                                         transfer_id=transfer.pk
                                                         )
                change_transmission_status = mailing.models.Transfer.objects.get(id=transfer.pk)
                change_transmission_status.status = "READY"
                change_transmission_status.save()

        # WEEKLY SCHEDULER
        today = datetime.today().weekday()
        if transfer.periodicity == "WEEKLY":
            print("TYPE: SEND WEEKLY")
            print("ID:", transfer.pk)
            convert_time = str(transfer.time)[:5]
            print("TIME:", convert_time)
            message = transfer.get_messages()
            print("MESSAGE THEME:", message.topic)
            print("MESSAGE BODY:", message.body)
            for client_mail in transfer.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)

                if today == 0:
                    schedule.every().sunday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                message_topic=message.topic, message_body=message.body,
                                                                transfer_id=transfer.pk)
                if today == 1:
                    schedule.every().monday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                message_topic=message.topic, message_body=message.body,
                                                                transfer_id=transfer.pk)
                if today == 2:
                    schedule.every().tuesday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                 message_topic=message.topic, message_body=message.body,
                                                                 transfer_id=transfer.pk)
                if today == 3:
                    schedule.every().wednesday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                   message_topic=message.topic,
                                                                   message_body=message.body,
                                                                   transfer_id=transfer.pk)
                if today == 4:
                    schedule.every().thursday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                  message_topic=message.topic,
                                                                  message_body=message.body,
                                                                  transfer_id=transfer.pk)
                if today == 5:
                    schedule.every().friday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                message_topic=message.topic, message_body=message.body,
                                                                transfer_id=transfer.pk)
                if today == 6:
                    schedule.every().saturday.at(convert_time).do(sendmails, emails_base=emails_base,
                                                                  message_topic=message.topic,
                                                                  message_body=message.body,
                                                                  transfer_id=transfer.pk)

                change_transfer_status = mailing.models.Transfer.objects.get(id=transfer.pk)
                change_transfer_status.status = "READY"
                change_transfer_status.save()

        # MONTHLY SCHEDULER
        if transfer.periodicity == "MONTHLY":
            print("TYPE: SEND MONTHLY")
            print("ID:", transfer.pk)
            convert_time = str(transfer.time)[:5]
            print("TIME:", convert_time)
            message = transfer.get_messages()
            print("MESSAGE THEME:", message.theme)
            print("MESSAGE BODY:", message.body)
            for client_mail in transfer.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)
                schedule.every(4).weeks.do(sendmails, emails_base=emails_base, message_topic=message.theme,
                                           message_body=message.body, transfer_id=transfer.pk)

                change_transfer_status = mailing.models.Transfer.objects.get(id=transfer.pk)
                change_transfer_status.status = "READY"
                change_transfer_status.save()

        print("ALL JOBS:")
        print(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)