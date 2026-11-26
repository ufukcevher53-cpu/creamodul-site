// ?kafe=Route Waffle → demoyu kafe adıyla gösterir
(function(){
  var q=new URLSearchParams(location.search).get("kafe"), n=null;
  try{ if(q){localStorage.setItem("cm_kafe",q);} n=q||localStorage.getItem("cm_kafe"); }catch(e){ n=q; }
  if(!n) return; n=n.trim().slice(0,40); if(!n) return;
  var up=n.toLocaleUpperCase("tr-TR"), ini=up.charAt(0);
  if(window.MENU&&MENU.brand) MENU.brand.name=n;
  function apply(){
    document.title=document.title.replace("Waffle oluşturucu demosu",n).replace("Kasa demosu",n+" · Kasa");
    var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),t;
    while(t=w.nextNode()){ var v=t.nodeValue; if(v.indexOf("ÖRNEK KAFE")>-1||v.indexOf("Örnek Kafe")>-1){ t.nodeValue=v.split("ÖRNEK KAFE").join(up).split("Örnek Kafe").join(n); } }
    document.querySelectorAll(".logo").forEach(function(e){ if(e.textContent.trim()==="Ö") e.textContent=ini; });
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",apply); else apply();
  new MutationObserver(function(ms){ ms.forEach(function(m){ m.addedNodes.forEach(function(x){ if(x.nodeType===1&&/ÖRNEK KAFE|Örnek Kafe/.test(x.textContent)) apply(); }); }); }).observe(document.documentElement,{childList:true,subtree:true});
})();
