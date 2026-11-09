(function(){
  'use strict';
  document.documentElement.classList.add('js');

  // Sticky header style on scroll
  var header=document.querySelector('.site-header');
  function onScroll(){header.classList.toggle('scrolled',window.scrollY>40);if(window.scrollY<window.innerHeight*.5)document.querySelectorAll('.primary-nav a.active').forEach(function(a){a.classList.remove('active');});}
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});

  // Mobile menu
  var toggle=document.querySelector('.nav-toggle'),nav=document.getElementById('primary-nav');
  function setMenu(open){
    toggle.setAttribute('aria-expanded',String(open));
    toggle.setAttribute('aria-label',open?'Close menu':'Open menu');
    nav.classList.toggle('open',open);
    document.body.style.overflow=open?'hidden':'';
  }
  toggle.addEventListener('click',function(){setMenu(toggle.getAttribute('aria-expanded')!=='true');});
  nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setMenu(false);});});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false);});

  // Reveal on scroll
  var heroItems=document.querySelectorAll('.hero .reveal');
  heroItems.forEach(function(el,i){el.style.setProperty('--i',i);});
  var items=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});
    },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    items.forEach(function(el){io.observe(el);});
  } else items.forEach(function(el){el.classList.add('in');});

  // Active nav link
  var links=[].slice.call(document.querySelectorAll('.primary-nav a[href^="#"]:not(.btn)'));
  var sections=links.map(function(l){return document.querySelector(l.getAttribute('href'));});
  if('IntersectionObserver' in window){
    var so=new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){var id='#'+en.target.id;links.forEach(function(l){l.classList.toggle('active',l.getAttribute('href')===id);});}
      });
    },{rootMargin:'-45% 0px -50% 0px'});
    sections.forEach(function(s){if(s)so.observe(s);});
  }

  // Opening hours: highlight today + open status (Helsinki time)
  var hours={0:null,1:[10,19],2:[10,19],3:[10,19],4:[10,20],5:[9,20],6:[9,16]};
  try{
    var parts=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Helsinki',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date());
    var map={};parts.forEach(function(p){map[p.type]=p.value;});
    var day=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(map.weekday);
    var h=parseInt(map.hour,10)%24+parseInt(map.minute,10)/60;
    var row=document.querySelector('.hours-table tr[data-day="'+day+'"]');if(row)row.classList.add('today');
    var st=document.getElementById('open-status'),t=hours[day];
    if(t&&h>=t[0]&&h<t[1]){st.textContent='Open now · until '+t[1]+':00';st.classList.add('open');}
    else{st.textContent='Closed right now';st.classList.add('closed');}
  }catch(e){}

  // Booking form (demo only)
  var form=document.getElementById('booking-form'),err=document.getElementById('form-error'),ok=document.getElementById('form-success');
  var date=document.getElementById('date');
  var today=new Date();today.setMinutes(today.getMinutes()-today.getTimezoneOffset());
  date.min=today.toISOString().slice(0,10);
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=[];
    form.querySelectorAll('[required]').forEach(function(f){
      var v=f.value.trim(),valid=!!v;
      if(f.type==='email')valid=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
      f.classList.toggle('invalid',!valid);f.setAttribute('aria-invalid',String(!valid));
      if(!valid)bad.push(f);
    });
    if(bad.length){err.textContent='Please fill in the highlighted fields.';err.hidden=false;bad[0].focus();return;}
    err.hidden=true;
    var name=form.name.value.trim().split(' ')[0];
    var d=new Date(form.date.value+'T12:00');
    var ds=d.toLocaleDateString('en-GB',{weekday:'long',day:'numeric',month:'long'});
    document.getElementById('success-name').textContent=', '+name;
    document.getElementById('success-text').textContent='Your request for '+form.service.value.split(' — ')[0]+' with '+(form.barber.value==='No preference'?'the first available barber':form.barber.value)+' on '+ds+' at '+form.time.value+' looks good.';
    ok.hidden=false;
    ok.querySelector('button').focus();
  });
  document.getElementById('booking-reset').addEventListener('click',function(){
    form.reset();ok.hidden=true;form.querySelectorAll('.invalid').forEach(function(f){f.classList.remove('invalid');});
    document.getElementById('name').focus();
  });

  document.getElementById('year').textContent=new Date().getFullYear();
})();
