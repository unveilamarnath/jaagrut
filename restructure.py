import os
import glob
from bs4 import BeautifulSoup, Comment

footer_html = """<footer>
  <div class="ft">
    <div>
      <div class="ft-name">Jaagrut<sup class="tm" style="color:#6B5A48;">™</sup></div>
      <div class="ft-tag">We shape the future. We teach.</div>
      <div class="ft-info">
        Jaagrut Educational Services Pvt Ltd<br>
        28 RBI Colony, Anandnagar, Bengaluru 560024<br>
        <a href="tel:+919620000535">+91 96200 00535</a> &nbsp;&middot;&nbsp;
        <a href="/cdn-cgi/l/email-protection#78191c151116381219191f0a0d0c561b1715"><span class="__cf_email__" data-cfemail="a9c8cdc4c0c7e9c3c8c8cedbdcdd87cac6c4">[email&#160;protected]</span></a>
      </div>
    </div>
    <ul class="ft-links"><li><a href="index.html">Home</a></li><li><a href="about.html">About</a></li><li><a href="how-we-work.html">How We Work</a></li><li><a href="enrol.html">Enrol</a></li><li><a href="book-diagnostic.html">Book Diagnostic</a></li><li><a href="grades-6-9.html">Grades 6–9</a></li><li><a href="cbse-10.html">10th CBSE</a></li><li><a href="icse-10.html">10th ICSE</a></li><li><a href="class-11-12.html">11th–12th</a></li><li><a href="jee-neet.html">JEE &amp; NEET</a></li><li><a href="kcet.html">KCET</a></li></ul>
    <div class="ft-legal">&copy; 2025 Jaagrut Educational Services Pvt Ltd<br>Google Rating: 4.8 &middot; Est. 2007</div>
  </div>
</footer>"""

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pre-clean weird footer truncation where a div is improperly followed by a script tag:
    # `<div class="ft-legal \n <script>` -> we can just regex this off since bs4 struggles a bit
    import re
    # Remove the broken ft-legal if it's there
    content = re.sub(r'<div class="ft-legal\s*<script', '<script', content)
    # Remove any stray parts of the old footer
    content = re.sub(r'<div class="ft-legal[^>]*>.*?</div>', '', content, flags=re.DOTALL)
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Replace the common style with link
    styles = soup.find_all('style')
    for style in styles:
        if style.string and '*,*::before,*::after{box-sizing:border-box' in style.string:
            link = soup.new_tag('link', rel='stylesheet', href='assets/css/style.css')
            style.replace_with(link)

    # 2. Extract common scripts
    scripts = soup.find_all('script')
    main_js_added = False
    for script in scripts:
        if script.string:
            if 'function toggleCb' in script.string:
                if not main_js_added:
                    new_script = soup.new_tag('script', src='assets/js/main.js')
                    script.replace_with(new_script)
                    main_js_added = True
                else:
                    script.decompose()
            elif 'var btn=document.getElementById(\'ham\');' in script.string:
                script.decompose()
    
    if not main_js_added:
        new_script = soup.new_tag('script', src='assets/js/main.js')
        soup.body.append(new_script)
        
    # 3. Handle footer
    if soup.footer:
        soup.footer.decompose()
        
    for class_name in ['ft', 'ft-name', 'ft-tag', 'ft-info', 'ft-links', 'ft-legal']:
        divs = soup.find_all(class_=class_name)
        for div in divs:
            div.decompose()
            
    footer_soup = BeautifulSoup(footer_html, 'html.parser')
    
    soup.body.append(footer_soup)
    
    # Re-order so scripts are after footer
    for script in soup.find_all('script'):
        if script.get('src') == 'assets/js/main.js' or (script.string and 'function sendCb' in script.string):
            script.extract()
            soup.body.append(script)

    with open(filepath, "w", encoding="utf-8") as f:
        # Use simple formatter to avoid too much spacing changes
        f.write(str(soup))
