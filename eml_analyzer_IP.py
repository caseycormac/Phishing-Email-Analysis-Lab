import re  # Import regular expressions module for pattern matching
from email import policy  # Email parsing policies for better handling of emails
from email.parser import BytesParser  # To parse raw email files

def analyze_eml(eml_path):
    # Open the email file in binary mode ('rb') and parse it into an email object
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Get all the email headers as a dictionary (e.g., From, To, Subject, Date)
    headers = dict(msg.items())
    # Get the full raw headers as a single string (for searching IP addresses)
    raw_headers = msg.as_string()

    # Extract important headers for display
    from_ = headers.get('From')       # Who sent the email
    to = headers.get('To')             # Who received the email
    subject = headers.get('Subject')   # The email's subject line
    date = headers.get('Date')         # When the email was sent

    # Get the main body of the email, prefer HTML but fall back to plain text
    body = msg.get_body(preferencelist=('html', 'plain'))
    # Extract the text content from the body or set to empty string if no body found
    body_text = body.get_content() if body else ''

    # Find all URLs in the email body using a regular expression pattern
    urls = re.findall(r'https?://[^\s"\'>]+', body_text)

    # Find all IP addresses in the raw headers using regex (pattern for IPv4)
    ips_in_headers = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', raw_headers)
    # Find all IP addresses in the email body text as well
    ips_in_body = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', body_text)

    # Initialize a list to hold any attachment filenames found
    attachments = []
    # Iterate over all attachments in the email (if any)
    for part in msg.iter_attachments():
        filename = part.get_filename()  # Get the attachment filename
        if filename:
            attachments.append(filename)  # Add it to the list if a filename exists

    # Now print all the collected information nicely

    print(f"From: {from_}")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Date: {date}\n")

    print("URLs found:")
    # Use set() to avoid duplicate URLs, then print each one
    for url in set(urls):
        print(f"- {url}")
    print()

    print("IP addresses found in headers:")
    for ip in set(ips_in_headers):
        print(f"- {ip}")
    print()

    print("IP addresses found in body:")
    for ip in set(ips_in_body):
        print(f"- {ip}")
    print()

    print("Attachments:")
    if attachments:
        # If attachments found, print each filename
        for a in attachments:
            print(f"- {a}")
    else:
        # Otherwise print 'None'
        print("None")

# This block runs when you execute the script directly from the command line
if __name__ == "__main__":
    import sys
    # Check if the user provided an email file as an argument
    if len(sys.argv) < 2:
        print("Usage: python3 eml_analyzer.py <file.eml>")
        sys.exit(1)  # Exit if no argument was given
    # Call the analyzer function with the filename passed as the first argument
    analyze_eml(sys.argv[1])
