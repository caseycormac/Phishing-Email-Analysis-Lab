# Phishing-Email-Analysis-Lab
A home Phishing Email Analysis Lab conducted in a Kali Linux Enviroment 

This is a Python tool made to analyze phishing emails saved as `.eml` files.  
It extracts and displays important indicators such as:

- Email headers (From, To, Subject, Date)  
- URLs found in the email body  
- IP addresses found in headers and body  
- Attachments included in the email  

## How to Use

1. Save your phishing email in `.eml` format.  
2. Run the script with Python 3:

   ```bash
   python3 eml_analyzer.py path/to/email.eml
