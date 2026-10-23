const $=s=>document.querySelector(s);
const btnUpload=$('#btn-upload'),fileIn=$('#file');
btnUpload.addEventListener('click',()=>fileIn.click());
fileIn.addEventListener('change',async()=>{
  if(!$('#consent').checked){alert('Consent required');return}
  const fd=new FormData();
  fd.append('file',fileIn.files[0]);
  fd.append('consent','true');
  fd.append('language','mr');
  fd.append('purpose','buying');
  try{
    const r=await fetch('/api/analyze',{method:'POST',body:fd});
    if(!r.ok){const e=await r.json();throw new Error(e.detail||r.statusText)}
    const d=await r.json();
    $('#upload').classList.remove('active');
    $('#results').classList.add('active');
    $('#summary').innerHTML=`<p>${d.explanation?.summary||''}</p>`;
    $('#flags').innerHTML=(d.flags||[]).map(f=>`<div class="flag-card ${f.severity}"><b>${f.title_mr}</b><p>${f.detail_mr}</p></div>`).join('');
    $('#checklist').innerHTML='<ol>'+(d.checklist||[]).map(c=>`<li>${c.title}</li>`).join('')+'</ol>';
  }catch(e){$('#err').textContent=e.message;$('#err').hidden=false}
});
