
(function(){
  const btn=document.querySelector('.menu-toggle');
  const panel=document.querySelector('.nav-links');
  if(btn&&panel){
    btn.addEventListener('click',()=>{
      const open=btn.getAttribute('aria-expanded')==='true';
      btn.setAttribute('aria-expanded',String(!open));
      panel.classList.toggle('is-open',!open);
    });
    panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
      btn.setAttribute('aria-expanded','false');panel.classList.remove('is-open');
    }));
  }
  const ba=document.querySelector('.ba');
  if(!ba)return;
  const wrap=ba.querySelector('.ba-before-wrap');
  const handle=ba.querySelector('.ba-handle');
  const range=ba.querySelector('.ba-range');
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function set(v){
    const pct=Math.max(0,Math.min(100,Number(v)));
    wrap.style.width=pct+'%';
    handle.style.left=pct+'%';
    range.value=String(pct);
  }
  range.addEventListener('input',e=>set(e.target.value));
  range.addEventListener('change',e=>set(e.target.value));
  function syncWidth(){
    const w=ba.clientWidth+'px';
    wrap.querySelectorAll('img').forEach(function(img){ img.style.width=w; img.style.maxWidth='none'; img.style.height='100%'; img.style.objectFit='cover'; });
  }
  syncWidth();
  window.addEventListener('resize',syncWidth);
  set(50);
})();
