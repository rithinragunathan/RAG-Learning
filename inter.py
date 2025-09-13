import requests
from bs4 import BeautifulSoup
url = "https://www.ilovepdf.com/pdf_to_word" # Replace with actual URL
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
pdf_links = []
for link in soup.find_all('a', href=True):
    if link['href'].endswith('.pdf'):
        pdf_links.append(link['href'])