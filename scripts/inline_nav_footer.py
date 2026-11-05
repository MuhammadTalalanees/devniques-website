"""Inline Navbar/Footer fragments into every page (run after editing assets/Navbar.html or assets/Footer.html).
Replaces the JS fetch (loadInto) with the static HTML + a small sync script that keeps
the burger toggle and the AI-page link rewrite. Bots then see nav/footer links without JS."""
import re, sys
from pathlib import Path

ROOT = Path('/home/hatch/workspace/devniques-website-work')
NAV = (ROOT / 'assets/Navbar.html').read_text()
FOOT = (ROOT / 'assets/Footer.html').read_text()

SYNC_SCRIPT = """<script>
(function(){
  // Navbar/footer are inlined in the HTML (no fetch), so every bot sees the links.
  var nav = document.getElementById('nav');
  if(nav){
    // On AI page, point fragment links back to homepage
    if(location.pathname.indexOf('ai-automation') !== -1){
      nav.querySelectorAll('a[href^="#"]').forEach(function(a){
        var h = a.getAttribute('href');
        if(h.length > 1) a.setAttribute('href', '/' + h);
      });
    }
    // Burger menu (null-safe)
    var burger = nav.querySelector('#burger');
    var links = nav.querySelector('#navLinks');
    if(burger && links){
      burger.addEventListener('click', function(){
        links.classList.toggle('open');
        document.getElementById('nav').classList.toggle('open');
      });
    }
  }
})();
</script>"""

FILES = ['index.html', 'ai-automation.html', 'blog.html', 'contact.html',
         'devniques-mdm.html', 'mdm-demo.html', 'microsoft-365.html',
         'ai-automation/index.html', 'blog/index.html', 'contact/index.html',
         'devniques-mdm/index.html', 'mdm-demo/index.html', 'microsoft-365/index.html']

for rel in FILES:
    p = ROOT / rel
    s = p.read_text()
    orig = s
    s = re.sub(r'<div id="navbar">\s*</div>', NAV.strip(), s, count=1)
    s = re.sub(r'<div id="footer">\s*</div>', FOOT.strip(), s, count=1)
    # replace the <script> block that defines loadInto with the sync script
    def _swap(m):
        return SYNC_SCRIPT if 'function loadInto' in m.group(0) else m.group(0)
    s = re.sub(r'<script>.*?</script>', _swap, s, count=0, flags=re.S)
    assert s != orig, f'no change in {rel}'
    assert 'loadInto' not in s, f'loadInto left in {rel}'
    assert '<div id="navbar">' not in s and '<div id="footer">' not in s, f'placeholder left in {rel}'
    assert 'Navbar.html?v=' not in s and 'Footer.html?v=' not in s, f'fetch left in {rel}'
    p.write_text(s)
    print(f'inlined {rel}')
print('OK: all 12 pages inlined')
