import os

# 1. Update style.css
style_path = 'assets/css/style.css'
with open(style_path, 'r', encoding='utf-8') as f:
    style_content = f.read()

style_content = style_content.replace('div.tm', '.team-bio')

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(style_content)

# 2. Update about.html
about_path = 'about.html'
with open(about_path, 'r', encoding='utf-8') as f:
    about_content = f.read()

# CSS replacements
about_content = about_content.replace('.tm{padding', '.team-bio{padding')
about_content = about_content.replace('.tm:last-child', '.team-bio:last-child')
about_content = about_content.replace('.tm.at ', '.team-bio.at ')
about_content = about_content.replace('.tm.qt ', '.team-bio.qt ')
about_content = about_content.replace(',.tm:last-child', ',.team-bio:last-child')

# HTML replacements
about_content = about_content.replace('class="tm at"', 'class="team-bio at"')
about_content = about_content.replace('class="tm qt"', 'class="team-bio qt"')

with open(about_path, 'w', encoding='utf-8') as f:
    f.write(about_content)

print("Renamed .tm to .team-bio completely to avoid trademark class collisions.")
