import sendgrid
import os
from sendgrid.helpers.mail import *
from project.settings import FROM_MAIL


def send_email(receipt,resident):
	
	content_str = f'Thank you Mr./Mrs. {resident.name} from {resident.flat_no} for your payment sum of Rs. {receipt.total_fee} only towards Maintenance Charges for the month {receipt.month} through online banking.'
		
	sg = sendgrid.SendGridAPIClient(api_key=env('SENDGRID_API_KEY'))	
	from_email = Email(FROM_MAIL)
	to_email = To(resident.email_id)
	subject = f'Society Management Receipt for the month {receipt.month}'
	
	content = Content("text/plain", content_str)
	mail = Mail(from_email, to_email, subject, content)
	print(content_str)
	sg.client.mail.send.post(request_body=mail.get())
