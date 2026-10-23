const $ = s => document.querySelector(s);
const btnUpload = $('#btn-upload'), fileIn = $('#file');
btnUpload.addEventListener('click', () => {
  if (!$('#consent').checked) { $('#err').textContent = 'कृपया संमती द्या / Please consent first.'; $('#err').hidden = false; return; }
  fileIn.click();
});

// ── Language switching ──────────────────────────────────────────
const LANG_LABELS = {
  mr: { mr: 'मराठी', hi: 'हिंदी', en: 'English' },
  hi: { mr: 'मराठी', hi: 'हिंदी', en: 'English' },
  en: { mr: 'मराठी', hi: 'हिंदी', en: 'English' },
};

const UI = {
  mr: {
    title: 'सातबारा साथी',
    tag: '७/१२ उतारा समजून घ्या',
    consent: 'मी समजतो/ते की हे केवळ माहितीसाठी आहे',
    upload: '📷 अपलोड / फोटो काढा',
    results: 'विश्लेषण',
    listen: '🔊 ऐका',
    disc: 'हे विश्लेषण केवळ माहितीसाठी आहे. कायदेशीर सल्ला नाही.',
    fb: 'स्पष्ट होते का?',
    fbYes: '✓ हो',
    fbNo: '✗ नाही',
    err: 'त्रुटी',
  },
  hi: {
    title: 'सातबारा साथी',
    tag: '७/१२ उतारा समझें घ्या',
    consent: 'मैं समझता/समझती हूँ कि यह केवल जानकारी के लिए है',
    upload: '📷 अपलोड / फोटो खींचें',
    results: 'विश्लेषण',
    listen: '🔊 सुनें',
    disc: 'यह विश्लेषण केवल जानकारी के लिए है। कानूनी सल्ला नहीं।',
    fb: 'स्पष्ट था क्या?',
    fbYes: '✓ हाँ',
    fbNo: '✗ नहीं',
    err: 'त्रुटि',
  },
  en: {
    title: 'Satbara Saathi',
    tag: 'Understand the 7/12 extract',
    consent: 'I understand this is for information only',
    upload: '📷 Upload / Take photo',
    results: 'Analysis',
    listen: '🔊 Listen',
    disc: 'This analysis is for information only. It is not legal advice.',
    fb: 'Was it clear?',
    fbYes: '✓ Yes',
    fbNo: '✗ No',
    err: 'Error',
  },
};

let currentLang = 'mr';
const langKey = l => (l === 'mr' ? 'mr' : l === 'hi' ? 'hi' : 'en');
const field = (obj, key) => obj[key] || obj.en || '';

function applyLang(lang) {
  currentLang = lang;
  document.documentElement.lang = lang === 'en' ? 'en' : lang === 'hi' ? 'hi' : 'mr';
  document.querySelectorAll('.lang-row button').forEach(b => {
    b.classList.toggle('on', b.dataset.lang === lang);
    b.textContent = LANG_LABELS[lang][b.dataset.lang];
  });
  const t = UI[lang];
  $('#upload h1').textContent = t.title;
  $('#upload .tag').textContent = t.tag;
  $('#consent').nextSibling.textContent = ' ' + t.consent;
  $('#btn-upload').textContent = t.upload;
  $('#results h2').textContent = t.results;
  $('#btn-listen').textContent = t.listen;
  $('.disc').textContent = t.disc;
  $('#fb-yes').textContent = t.fbYes;
  $('#fb-no').textContent = t.fbNo;
  $('#err').textContent = t.err;
  $('#err').hidden = true;
}

document.querySelectorAll('.lang-row button').forEach(b => {
  b.addEventListener('click', () => applyLang(b.dataset.lang));
});
applyLang('mr');

fileIn.addEventListener('change', async () => {
  if (!$('#consent').checked) { alert('Consent required'); return; }
  const fd = new FormData();
  fd.append('file', fileIn.files[0]);
  fd.append('consent', 'true');
  fd.append('language', currentLang);
  fd.append('purpose', 'buying');
  try {
    const r = await fetch('/api/analyze', { method: 'POST', body: fd });
    if (!r.ok) { const e = await r.json(); throw new Error(e.detail || r.statusText); }
    const d = await r.json();
    $('#upload').classList.remove('active');
    $('#results').classList.add('active');
    $('#summary').innerHTML = `<p>${d.explanation?.summary || ''}</p>`;
    $('#flags').innerHTML = (d.flags || []).map(f => {
      const k = langKey(currentLang);
      return `<div class="flag-card ${f.severity}"><b>${field(f, 'title_' + k)}</b>
       <p>${field(f, 'detail_' + k)}</p></div>`;
    }).join('');
    $('#checklist').innerHTML = '<ol>' + (d.checklist || []).map(c => `<li>${c.title}</li>`).join('') + '</ol>';
  } catch (e) { $('#err').textContent = e.message; $('#err').hidden = false; }
});