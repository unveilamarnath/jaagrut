import os
import glob
from bs4 import BeautifulSoup

mob_menu_html_template = """<div class="mob-menu" id="mob-nav">
<a href="index.html">Home</a>
<a href="about.html">About</a>
<a href="how-we-work.html">How We Work</a>
<a href="enrol.html">Enrol</a>
<a href="book-diagnostic.html">Book Diagnostic</a>
<a href="courses.html">Courses</a>
<a href="grades-6-9.html">Grades 6–9</a>
<a href="cbse-10.html">10th CBSE</a>
<a href="icse-10.html">10th ICSE</a>
<a href="class-11-12.html">Classes 11–12</a>
<a href="jee-neet.html">JEE &amp; NEET</a>
<a href="kcet.html">KCET</a>
<a href="faq.html">FAQs</a>
<a class="mob-menu-cta" href="book-diagnostic.html">Schedule a Diagnostic Test →</a>
</div>"""

for filepath in glob.glob("*.html"):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    modified = False

    nav = soup.find('nav')
    if nav:
        # Add hamburger button inside nav if not present
        if not nav.find(id='ham'):
            ham_btn = soup.new_tag('button', id='ham', attrs={'class': 'ham-btn'})
            for _ in range(3):
                span = soup.new_tag('span')
                ham_btn.append(span)
            nav.append(ham_btn)
            modified = True

        # Check if mob-menu exists
        mob_nav = soup.find(id='mob-nav')
        if not mob_nav:
            mob_menu_soup = BeautifulSoup(mob_menu_html_template, 'html.parser')
            mob_div = mob_menu_soup.div
            
            # Set active class on mobile menu
            for a_tag in mob_div.find_all('a'):
                if a_tag.get('href') == filename:
                    a_tag['class'] = a_tag.get('class', []) + ['on']

            # Insert right after nav
            nav.insert_after(mob_div)
            modified = True
            
        # Also ensure desktop nav has the correct active link
        nm = nav.find('ul', class_='nm')
        if nm:
            for a_tag in nm.find_all('a'):
                # remove 'on' class from all
                if 'on' in a_tag.get('class', []):
                    a_tag['class'] = [c for c in a_tag['class'] if c != 'on']
                # add 'on' to the matching filename
                if a_tag.get('href') == filename:
                    a_tag['class'] = a_tag.get('class', []) + ['on']
            modified = True
            
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
