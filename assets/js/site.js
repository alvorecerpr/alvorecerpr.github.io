/* Site da Alvorecer - menu do celular, marcadores de pendência da prévia, cópia da chave Pix e formulários */
(function(){
  document.documentElement.classList.remove('no-js');

  /* menu no celular */
  var nav = document.getElementById('mainNav'), menuBtn = document.getElementById('menuBtn');
  if(nav && menuBtn){
    menuBtn.addEventListener('click', function(){
      var o = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && nav.classList.contains('open')){ nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded','false'); menuBtn.focus(); }
    });
  }

  /* marcadores de pendência (só na prévia) */
  var tg = document.getElementById('togglePend');
  if(tg){
    try{ if(localStorage.getItem('alv-pend') === '0'){ tg.checked = false; } }catch(e){}
    var applyPend = function(){
      document.body.classList.toggle('hide-pend', !tg.checked);
      try{ localStorage.setItem('alv-pend', tg.checked ? '1' : '0'); }catch(e){}
    };
    tg.addEventListener('change', applyPend); applyPend();
  }

  /* assunto do formulário de contato vindo do link (?assunto=...) */
  var sel = document.getElementById('c-assunto');
  if(sel){
    try{
      var a = new URLSearchParams(location.search).get('assunto');
      if(a){ for(var i=0;i<sel.options.length;i++){ if(sel.options[i].text === a){ sel.selectedIndex = i; break; } } }
    }catch(e){}
  }

  /* Pix */
  var copy = document.getElementById('copyPix');
  if(copy){
    copy.addEventListener('click', function(){
      var key = document.getElementById('pixKey'), m = document.getElementById('pixMsg');
      var k = key.textContent.trim();
      function fallback(){ var r=document.createRange(); r.selectNodeContents(key); var s=getSelection(); s.removeAllRanges(); s.addRange(r); m.textContent='Chave selecionada. Use Ctrl+C para copiar.'; }
      try{ navigator.clipboard.writeText(k).then(function(){ m.textContent='Chave copiada.'; }, fallback); }catch(e){ fallback(); }
    });
  }

  /* formulários: enquanto o serviço de envio não for escolhido, mostram o aviso em vez de enviar */
  document.querySelectorAll('form[data-ok]').forEach(function(f){
    f.addEventListener('submit', function(e){
      if(f.getAttribute('action')) return;
      e.preventDefault();
      var ok = document.getElementById(f.getAttribute('data-ok'));
      if(ok){ ok.classList.add('show'); ok.focus(); }
    });
  });
})();
