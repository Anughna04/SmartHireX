"""class InterviewScheduler:
    def generate_invite(self, candidate_name, email, job_title):
        return f"Hello {candidate_name},\n\nYou have been shortlisted for the {job_title} role. Please reply with your availability for an interview this week.\n\nThanks,\nRecruitment Team"
"""
import smtplib
from email.mime.text import MIMEText

def send_email_invites(name, email):
    sender = "your_email@gmail.com"
    password = "your_app_password"  # Use App Password if 2FA is on
    subject = "Interview Invitation"
    body = f"Hi {name},\n\nCongratulations! You’ve been shortlisted. We'd like to invite you for an interview.\n\nBest,\nHR Team"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [email], msg.as_string())
        server.quit()
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
