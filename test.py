import requests, re
from bs4 import BeautifulSoup

url = "https://mercyrelief.org.uk/en/fundraising/university-of-birmingham-isoc/1000105-ubisoc-gaza-appeal"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, "lxml")

component = soup.find("n3o-crowdfunder-progress")
print(f"Component in static HTML: {component is not None}")
if component:
    print(component)
else:
    amounts = re.findall(r'£[\d,]+', r.text)
    print(f"£ amounts found: {amounts}")