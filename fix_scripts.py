import glob
from bs4 import BeautifulSoup

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # Check if main.js exists
    has_main_js = False
    for script in soup.find_all('script'):
        if script.get('src') == 'assets/js/main.js':
            has_main_js = True
            break
            
    if not has_main_js:
        # Also clean up old inline scripts that we might have missed
        for script in soup.find_all('script'):
            text = script.get_text()
            if 'function toggleCb' in text or 'var btn=document.getElementById(\'ham\')' in text:
                script.decompose()
        
        # Append main.js
        new_script = soup.new_tag('script', src='assets/js/main.js')
        if soup.body:
            soup.body.append(new_script)
        else:
            soup.append(new_script)
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
