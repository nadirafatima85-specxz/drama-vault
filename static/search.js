(function(){var d=window.__DRAMAS__;if(!d)return;var f=document.getElementById('f'),out=document.getElementById('results'),st=document.getElementById('status'),per=12,page=1;
function val(n){return f.elements[n].value}
function run(){var q=val('q').toLowerCase().trim(),dec=val('decade'),g=val('genre'),b=val('broadcaster'),s=val('sort');
var r=d.filter(function(x){return(!q||(x.title+' '+x.alt.join(' ')+' '+x.cast.join(' ')).toLowerCase().indexOf(q)>-1)&&(!dec||String(Math.floor(x.year/10)*10)===dec)&&(!g||x.genre.indexOf(g)>-1)&&(!b||x.b===b)});
r.sort(function(a,c){return s==='title'?a.title.localeCompare(c.title):s==='new'?c.year-a.year:a.year-c.year});
var pages=Math.max(1,Math.ceil(r.length/per));if(page>pages)page=pages;var sl=r.slice((page-1)*per,page*per);
out.innerHTML=sl.map(function(x){return'<li><a class="card" style="display:block;text-decoration:none;color:inherit" href="/dramas/'+x.slug+'/"><h3>'+x.title.replace(/</g,'&lt;')+'</h3><p class="meta">'+x.year+' · '+x.bn+'</p></a></li>'}).join('');
st.textContent=r.length?r.length+' drama'+(r.length>1?'s':'')+' found. Page '+page+' of '+pages+'.':'No dramas match these filters. Try removing a filter or use Reset.';
document.getElementById('prev').disabled=page<=1;document.getElementById('next').disabled=page>=pages}
f.addEventListener('input',function(){page=1;run()});f.addEventListener('submit',function(e){e.preventDefault();run()});
f.addEventListener('reset',function(){page=1;setTimeout(run)});
document.getElementById('prev').onclick=function(){page--;run()};document.getElementById('next').onclick=function(){page++;run()};
document.querySelectorAll('.jsonly').forEach(function(e){e.hidden=false});run()})();
