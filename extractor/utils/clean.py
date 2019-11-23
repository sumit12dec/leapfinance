from ..settings import INVALID_EMAIL_ENDS

def clean_emails(emails):
	cleaned_emails = []

	for email in emails:
		if email.split('.')[-1] not in INVALID_EMAIL_ENDS:
			cleaned_emails.append(email)
	return cleaned_emails

def clean_images(images):
	cleaned_images = []
	for img in images:
		if img.split('.')[-1] in INVALID_EMAIL_ENDS:
			cleaned_images.append(img)
	return cleaned_images

def clean_text(text):
	return text.strip()