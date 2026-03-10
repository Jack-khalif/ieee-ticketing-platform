from celery import shared_task


@shared_task
def send_ticket_email(user_email, ticket_id):

    print(f"Sending ticket {ticket_id} to {user_email}")

    return "Email sent"