from bs4 import BeautifulSoup

with open('test.html', 'r', encoding='utf8') as f:
    bs = BeautifulSoup(f.read(), 'lxml')
    text = bs.find(id='activity-name').text
    print(text.strip())
