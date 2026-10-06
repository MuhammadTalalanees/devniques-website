// ===== Shared navbar/footer loader (single source of truth) =====
(function(){
  function loadComponent(url, targetId){
    fetch(url).then(r=>r.text()).then(html=>{
      const target = document.getElementById(targetId);
      if(target) target.innerHTML = html;
      // Re-run nav JS after navbar loads
      if(targetId === 'nav-slot'){
        document.querySelectorAll('#nav-slot a[data-nav]').forEach(a=>{
          a.addEventListener('click',e=>{
            const href=a.getAttribute('href'),parts=href.split('#'),page=parts[0],hash=parts[1];
            const cur=(location.pathname.split('/').pop()||'index.html');
            if(hash&&(page===''||page===cur||(cur===''&&page==='index.html'))){
              const el=document.getElementById(hash);
              if(el){e.preventDefault();el.scrollIntoView({behavior:'smooth'});}
            }
          });
        });
        // Burger menu
        const burger = document.getElementById('burger');
        const navLinks = document.getElementById('navLinks');
        if(burger && navLinks){
          burger.addEventListener('click', ()=> navLinks.classList.toggle('open'));
        }
        // Logo -> homepage
        const brand = document.querySelector('#nav-slot .brand');
        if(brand){
          brand.addEventListener('click', e=>{
            e.preventDefault();
            location.href = 'index.html';
          });
        }
      }
    }).catch(()=>{});
  }
  document.addEventListener('DOMContentLoaded', ()=>{
    loadComponent('components/navbar.html', 'nav-slot');
    loadComponent('components/footer.html', 'footer-slot');
  });
})();
