
(function(){
  const btn=document.querySelector('.menu-toggle');
  const panel=document.querySelector('.nav-links');
  if(!btn||!panel)return;
  btn.addEventListener('click',()=>{
    const open=btn.getAttribute('aria-expanded')==='true';
    btn.setAttribute('aria-expanded',String(!open));
    panel.classList.toggle('is-open',!open);
  });
  panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
    btn.setAttribute('aria-expanded','false');panel.classList.remove('is-open');
  }));
})();
