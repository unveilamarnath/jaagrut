function toggleCb(id){
  var el=document.getElementById(id);
  if(el){el.style.display=el.style.display==='none'?'block':'none';}
}

function sendCb(id,page){
  var nEl = document.getElementById('cb-n-'+id);
  var pEl = document.getElementById('cb-p-'+id);
  var eEl = document.getElementById('cb-e-'+id);
  var mEl = document.getElementById('cb-m-'+id);

  var name = nEl ? nEl.value.trim() : "";
  var phone = pEl ? pEl.value.trim() : "";
  var email = eEl ? eEl.value.trim() : "";
  var msg = mEl ? mEl.value.trim() : "";

  if(!name||!phone){
    alert('Please enter your name and phone number.');
    return;
  }

  var txt='Callback request — Jaagrut%0A---%0AName: '+encodeURIComponent(name)+'%0APhone: '+encodeURIComponent(phone)+'%0AEmail: '+encodeURIComponent(email||'Not provided')+'%0AMessage: '+encodeURIComponent(msg||'None')+'%0APage: '+encodeURIComponent(page);
  window.open('https://wa.me/919620000535?text='+txt,'_blank');

  var dEl = document.getElementById('cb-done-'+id);
  if(dEl){dEl.style.display='block';}
}

(function(){
  var btn=document.getElementById('ham');
  var menu=document.getElementById('mob-nav');
  if(!btn||!menu)return;
  btn.addEventListener('click',function(){
    btn.classList.toggle('open');
    menu.classList.toggle('open');
  });
  menu.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click',function(){
      btn.classList.remove('open');
      menu.classList.remove('open');
    });
  });
})();
