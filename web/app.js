/* ============================================================
   Satbara Saathi — front-end
   Vanilla JS, no build step, no CDN. Runs offline and on a phone.
   ============================================================ */
'use strict';

// ── TODO: edit these two values once — they appear in the banner and footer ──
const BRAND = { team: '[Team Name]', event: '[Hackathon Name]' };

const MAX_BYTES = 10 * 1024 * 1024; // must match MAX_FILE_SIZE in app/pipeline/preprocess.py

/* ── Translations ───────────────────────────────────────────
   Every element with data-i18n="key" is filled from here.
   Placeholders: {team} {event} {n} {lang} {done} {total}        */
const UI = {
  mr: {
    skip: 'थेट मुख्य भागात जा',
    brand: 'सातबारा साथी', brand_sub: 'Satbara Saathi',
    hack_title: 'हॅकेथॉन प्रोजेक्ट', hack_event: '{event} 2026', proto: 'प्रोटोटाइप',

    hero_badge: '७/१२ समजून घेण्यासाठी मोफत साधन',
    hero_title: 'तुमचा ७/१२ उतारा सोप्या भाषेत समजून घ्या',
    hero_sub: 'उताऱ्याचा फोटो अपलोड करा. आम्ही त्यावरील मजकूर वाचून महत्त्वाचे मुद्दे सोप्या भाषेत समजावतो. खाते नाही, शुल्क नाही.',

    drop_title: '७/१२ चा फोटो इथे टाका',
    drop_sub: 'फाइल इथे ओढून सोडा किंवा खालील बटणावरून निवडा',
    drop_btn: 'फाइल निवडा', drop_camera: 'फोटो काढा',
    drop_hint: 'JPG किंवा PNG · जास्तीत जास्त १० MB · फोटो स्पष्ट असावा',
    drop_locked: 'अपलोड करण्यापूर्वी खालील संमतीची चौकट खूण करा.',
    consent: 'हे साधन फक्त माहितीसाठी आहे आणि कायदेशीर सल्ला नाही, हे मी समजतो/समजते.',

    trust1_h: 'तुमची माहिती सुरक्षित',
    trust1_b: 'उतारा फक्त विश्लेषणासाठी वापरला जातो आणि नंतर हटवला जातो. खाते तयार करावे लागत नाही.',
    trust2_h: 'कायदेशीर सल्ला नाही',
    trust2_b: 'हे साधन समजून घेण्यासाठी आहे. कोणताही व्यवहार करण्यापूर्वी तलाठी किंवा वकिलांकडून खात्री करा.',
    trust3_h: 'अधिकृत नोंदीशी पडताळा',
    trust3_b: 'निकाल महाभूलेख वरील अधिकृत ७/१२ शी जुळवून पाहा.',

    how_sum: 'हे कसे काम करते?',
    how1: 'तुम्ही ७/१२ चा फोटो अपलोड करता.',
    how2: 'आम्ही त्यावरील मजकूर वाचतो.',
    how3: 'ठराविक नियमांवर धोक्याचे मुद्दे तपासले जातात.',
    how4: 'AI ते सोप्या भाषेत समजावतो — पडताळणी तुम्ही अधिकृत नोंदीशी करता.',

    analyzing_title: 'तुमचा उतारा तपासत आहोत…',
    analyzing_sub: 'कृपया थोडे थांबा. हे पान सोडू नका.',
    stage1: 'फाइल तपासत आहोत',
    stage2: 'उताऱ्यावरील मजकूर वाचत आहोत',
    stage3: 'ठराविक नियमांवर तपासणी',
    stage4: 'सोप्या भाषेत समजावत आहोत',

    res_title: 'विश्लेषण', new_analysis: 'नवीन उतारा',
    verdict_kicker: 'नियमांवर आधारित तपासणी',
    verdict_src: 'हे ठराविक नियमांवर आधारित आहे, AI वर नाही.',
    v_serious_t: 'लक्ष देण्यासारखे मुद्दे आढळले',
    v_serious_b: '{n} गंभीर मुद्दे आढळले आहेत. पैसे देण्यापूर्वी किंवा करार करण्यापूर्वी हे मुद्दे तपासून घ्या.',
    v_check_t: 'काही मुद्दे तपासावे लागतील',
    v_check_b: 'गंभीर मुद्दे आढळले नाहीत, पण {n} मुद्दे तपासावे लागतील.',
    v_clear_t: 'ठळक मुद्दे आढळले नाहीत',
    v_clear_b: 'या उताऱ्यात नियमांवर आधारित ठळक मुद्दे आढळले नाहीत. याचा अर्थ जमीन निर्दोष आहे असा होत नाही — अधिकृत नोंदीशी पडताळणी करा.',

    count_serious: 'गंभीर', count_check: 'तपासणी', count_info: 'माहिती',
    sev_serious: 'गंभीर', sev_check: 'तपासणी', sev_info: 'माहिती',

    sec_summary: 'सोप्या भाषेत सारांश',
    ai_badge: '🤖 AI ने तयार केलेले · अधिकृत दस्तऐवज नाही',
    lang_note: 'AI सारांश {lang} मध्ये तयार झाला. भाषा बदलल्यावर तो बदलत नाही.',
    lang_mr: 'मराठी', lang_hi: 'हिंदी', lang_en: 'इंग्रजी',
    listen: 'ऐका', listen_stop: 'थांबा', copy: 'नक्कल करा', print: 'छापा', copied: 'नक्कल झाले',

    sec_flags: 'आढळलेले मुद्दे', no_flags: 'नियमांवर आधारित कोणतेही मुद्दे आढळले नाहीत.',
    todo: 'काय करावे', evidence: 'पुरावा', rule_label: 'नियम',

    sec_checklist: 'पुढील पावले', checklist_sub: 'प्रत्येक पावल पूर्ण झाल्यावर खूण करा.',
    done_count: '{done}/{total} पूर्ण',

    sec_quality: 'फोटोची गुणवत्ता', quality_ok: 'फोटोची गुणवत्ता विश्लेषणासाठी पुरेशी आहे.',
    q_blur: 'स्पष्टता', q_bright: 'प्रकाश', q_texture: 'मजकूर स्पष्टता', q_overall: 'एकूण',
    q_good: 'चांगले', q_fair: 'बरे', q_poor: 'कमी',

    sec_errors: 'तपासणीत आढळलेल्या त्रुटी',

    verify_pre: '⚠️ AI कधी कधी चुकू शकतो. महत्त्वाच्या व्यवहारापूर्वी',
    verify_link: 'महाभूलेख', verify_post: 'वर किंवा तलाठी कार्यालयात खात्री करा.',
    fb: 'हे स्पष्ट होते का?', fbYes: '✓ हो', fbNo: '✗ नाही', fb_thanks: 'अभिप्रायाबद्दल धन्यवाद!',

    foot_by: '{team} ने बनवले · {event} 2026', foot_gh: 'GitHub वर पाहा',
    foot_ver: 'v0.1 प्रोटोटाइप',
    foot_limit: 'मर्यादा: हस्तलिखित किंवा अस्पष्ट उतारे चुकीचे वाचले जाऊ शकतात.',

    err_network: 'सर्व्हरशी संपर्क होऊ शकला नाही. इंटरनेट तपासून पुन्हा प्रयत्न करा.',
    err_consent: 'पुढे जाण्यासाठी संमतीची चौकट खूण करा.',
    err_too_big: 'फाइल १० MB पेक्षा मोठी आहे. लहान फोटो निवडा.',
    err_type: 'फक्त JPG किंवा PNG फोटो चालतात.',
    err_generic: 'काहीतरी चूक झाली. पुन्हा प्रयत्न करा.',
    err_speech: 'या ब्राउझरमध्ये वाचन सुविधा नाही.',
  },

  hi: {
    skip: 'सीधे मुख्य भाग पर जाएँ',
    brand: 'सातबारा साथी', brand_sub: 'Satbara Saathi',
    hack_title: 'हैकथॉन प्रोजेक्ट', hack_event: '{event} 2026', proto: 'प्रोटोटाइप',

    hero_badge: '७/१२ समझने का मुफ़्त साधन',
    hero_title: 'अपना ७/१२ उतारा आसान भाषा में समझें',
    hero_sub: 'उतारे की फ़ोटो अपलोड करें। हम उस पर लिखा पाठ पढ़कर ज़रूरी बातें आसान भाषा में समझाते हैं। खाता नहीं, शुल्क नहीं।',

    drop_title: '७/१२ की फ़ोटो यहाँ डालें',
    drop_sub: 'फ़ाइल यहाँ खींचकर छोड़ें या नीचे के बटन से चुनें',
    drop_btn: 'फ़ाइल चुनें', drop_camera: 'फ़ोटो खींचें',
    drop_hint: 'JPG या PNG · अधिकतम १० MB · फ़ोटो साफ़ होनी चाहिए',
    drop_locked: 'अपलोड करने से पहले नीचे सहमति के बॉक्स पर टिक करें।',
    consent: 'यह साधन केवल जानकारी के लिए है और कानूनी सलाह नहीं है, यह मैं समझता/समझती हूँ।',

    trust1_h: 'आपकी जानकारी सुरक्षित',
    trust1_b: 'उतारा केवल विश्लेषण के लिए इस्तेमाल होता है और बाद में हटा दिया जाता है। खाता बनाने की ज़रूरत नहीं।',
    trust2_h: 'कानूनी सलाह नहीं',
    trust2_b: 'यह टूल समझने में मदद के लिए है। कोई भी लेन-देन करने से पहले तलाठी या वकील से पुष्टि करें।',
    trust3_h: 'आधिकारिक रिकॉर्ड से मिलान करें',
    trust3_b: 'नतीजों को महाभूलेख पर उपलब्ध आधिकारिक ७/१२ से मिलाकर देखें।',

    how_sum: 'यह कैसे काम करता है?',
    how1: 'आप ७/१२ की फ़ोटो अपलोड करते हैं।',
    how2: 'हम उस पर लिखा पाठ पढ़ते हैं।',
    how3: 'तय नियमों पर जोखिम वाले बिंदु जाँचे जाते हैं।',
    how4: 'AI उसे आसान भाषा में समझाता है — पुष्टि आप आधिकारिक रिकॉर्ड से करते हैं।',

    analyzing_title: 'आपका उतारा जाँचा जा रहा है…',
    analyzing_sub: 'कृपया थोड़ा इंतज़ार करें। यह पेज न छोड़ें।',
    stage1: 'फ़ाइल जाँची जा रही है',
    stage2: 'उतारे का पाठ पढ़ा जा रहा है',
    stage3: 'तय नियमों पर जाँच',
    stage4: 'आसान भाषा में समझाया जा रहा है',

    res_title: 'विश्लेषण', new_analysis: 'नया उतारा',
    verdict_kicker: 'नियम-आधारित जाँच',
    verdict_src: 'यह तय नियमों पर आधारित है, AI पर नहीं।',
    v_serious_t: 'ध्यान देने योग्य बिंदु मिले',
    v_serious_b: '{n} गंभीर बिंदु मिले हैं। पैसे देने या सौदा करने से पहले इन्हें जाँच लें।',
    v_check_t: 'कुछ बिंदु जाँचने होंगे',
    v_check_b: 'गंभीर बिंदु नहीं मिले, लेकिन {n} बिंदु जाँचने होंगे।',
    v_clear_t: 'कोई बड़ा बिंदु नहीं मिला',
    v_clear_b: 'इस उतारे में नियम-आधारित कोई बड़ा बिंदु नहीं मिला। इसका मतलब यह नहीं कि ज़मीन निर्दोष है — आधिकारिक रिकॉर्ड से मिलान करें।',

    count_serious: 'गंभीर', count_check: 'जाँच', count_info: 'जानकारी',
    sev_serious: 'गंभीर', sev_check: 'जाँच', sev_info: 'जानकारी',

    sec_summary: 'आसान भाषा में सार',
    ai_badge: '🤖 AI द्वारा तैयार · आधिकारिक दस्तावेज़ नहीं',
    lang_note: 'AI सार {lang} में बनाया गया। भाषा बदलने पर यह नहीं बदलता।',
    lang_mr: 'मराठी', lang_hi: 'हिंदी', lang_en: 'अंग्रेज़ी',
    listen: 'सुनें', listen_stop: 'रोकें', copy: 'कॉपी करें', print: 'प्रिंट करें', copied: 'कॉपी हो गया',

    sec_flags: 'मिले बिंदु', no_flags: 'नियम-आधारित कोई बिंदु नहीं मिला।',
    todo: 'क्या करें', evidence: 'प्रमाण', rule_label: 'नियम',

    sec_checklist: 'आगे के कदम', checklist_sub: 'हर कदम पूरा होने पर टिक करें।',
    done_count: '{done}/{total} पूरे',

    sec_quality: 'फ़ोटो की गुणवत्ता', quality_ok: 'फ़ोटो की गुणवत्ता विश्लेषण के लिए पर्याप्त है।',
    q_blur: 'स्पष्टता', q_bright: 'रोशनी', q_texture: 'पाठ की स्पष्टता', q_overall: 'कुल',
    q_good: 'अच्छी', q_fair: 'ठीक', q_poor: 'कम',

    sec_errors: 'जाँच में मिली त्रुटियाँ',

    verify_pre: '⚠️ AI कभी-कभी ग़लती कर सकता है। किसी महत्वपूर्ण लेन-देन से पहले',
    verify_link: 'महाभूलेख', verify_post: 'पर या तलाठी कार्यालय में पुष्टि करें।',
    fb: 'यह साफ़ समझ आया?', fbYes: '✓ हाँ', fbNo: '✗ नहीं', fb_thanks: 'प्रतिक्रिया के लिए धन्यवाद!',

    foot_by: '{team} द्वारा निर्मित · {event} 2026', foot_gh: 'GitHub पर देखें',
    foot_ver: 'v0.1 प्रोटोटाइप',
    foot_limit: 'सीमा: हस्तलिखित या धुंधले उतारे ग़लत पढ़े जा सकते हैं।',

    err_network: 'सर्वर से संपर्क नहीं हो सका। इंटरनेट जाँचकर फिर कोशिश करें।',
    err_consent: 'आगे बढ़ने के लिए सहमति के बॉक्स पर टिक करें।',
    err_too_big: 'फ़ाइल १० MB से बड़ी है। छोटी फ़ोटो चुनें।',
    err_type: 'केवल JPG या PNG फ़ोटो चलती हैं।',
    err_generic: 'कुछ गड़बड़ हो गई। फिर कोशिश करें।',
    err_speech: 'इस ब्राउज़र में पढ़ने की सुविधा नहीं है।',
  },

  en: {
    skip: 'Skip to main content',
    brand: 'Satbara Saathi', brand_sub: 'सातबारा साथी',
    hack_title: 'Hackathon project', hack_event: '{event} 2026', proto: 'Prototype',

    hero_badge: 'Free tool to understand your 7/12',
    hero_title: 'Understand your 7/12 extract in plain language',
    hero_sub: 'Upload a photo of your extract. We read the text and explain what matters in simple words. No account, no fee.',

    drop_title: 'Drop a photo of your 7/12 here',
    drop_sub: 'Drag the file here, or pick it with the buttons below',
    drop_btn: 'Choose a file', drop_camera: 'Take a photo',
    drop_hint: 'JPG or PNG · up to 10 MB · the photo should be sharp',
    drop_locked: 'Tick the consent box below before uploading.',
    consent: 'I understand this tool is for information only and is not legal advice.',

    trust1_h: 'Your information is safe',
    trust1_b: 'The extract is used only for analysis and deleted afterwards. No account is needed.',
    trust2_h: 'Not legal advice',
    trust2_b: 'This tool helps you understand. Confirm with the talathi or a lawyer before any transaction.',
    trust3_h: 'Check against official records',
    trust3_b: 'Compare the results with the official 7/12 on Mahabhulekh.',

    how_sum: 'How does it work?',
    how1: 'You upload a photo of your 7/12.',
    how2: 'We read the text on it.',
    how3: 'Fixed rules check for known red flags.',
    how4: 'AI explains it in plain language — you verify it against the official record.',

    analyzing_title: 'Checking your extract…',
    analyzing_sub: 'This takes a moment. Please stay on this page.',
    stage1: 'Checking the file',
    stage2: 'Reading the text',
    stage3: 'Running the rule checks',
    stage4: 'Explaining it in plain language',

    res_title: 'Analysis', new_analysis: 'New extract',
    verdict_kicker: 'Rule-based check',
    verdict_src: 'This comes from fixed rules, not from AI.',
    v_serious_t: 'Things need your attention',
    v_serious_b: '{n} serious issue(s) found. Look into these before paying or signing anything.',
    v_check_t: 'A few things to check',
    v_check_b: 'No serious issues found, but {n} item(s) are worth checking.',
    v_clear_t: 'No major issues found',
    v_clear_b: 'The rule checks found no major issues in this extract. That does not mean the land is clear — verify it against the official record.',

    count_serious: 'Serious', count_check: 'To check', count_info: 'Info',
    sev_serious: 'Serious', sev_check: 'Check', sev_info: 'Info',

    sec_summary: 'Plain-language summary',
    ai_badge: '🤖 Generated by AI · Not an official document',
    lang_note: 'The AI summary was generated in {lang}. It does not change when you switch language.',
    lang_mr: 'Marathi', lang_hi: 'Hindi', lang_en: 'English',
    listen: 'Listen', listen_stop: 'Stop', copy: 'Copy', print: 'Print', copied: 'Copied',

    sec_flags: 'What we found', no_flags: 'The rule checks found nothing to flag.',
    todo: 'What to do', evidence: 'Evidence', rule_label: 'Rule',

    sec_checklist: 'Next steps', checklist_sub: 'Tick each step as you complete it.',
    done_count: '{done}/{total} done',

    sec_quality: 'Photo quality', quality_ok: 'The photo is good enough to analyse.',
    q_blur: 'Sharpness', q_bright: 'Lighting', q_texture: 'Text clarity', q_overall: 'Overall',
    q_good: 'Good', q_fair: 'Fair', q_poor: 'Poor',

    sec_errors: 'Issues found while reading the document',

    verify_pre: '⚠️ AI can make mistakes. Before any important transaction, check on',
    verify_link: 'Mahabhulekh', verify_post: 'or at the talathi office.',
    fb: 'Was this clear?', fbYes: '✓ Yes', fbNo: '✗ No', fb_thanks: 'Thanks for the feedback!',

    foot_by: 'Built by {team} · {event} 2026', foot_gh: 'View on GitHub',
    foot_ver: 'v0.1 prototype',
    foot_limit: 'Limitation: handwritten or blurry extracts may be misread.',

    err_network: 'Could not reach the server. Check your connection and try again.',
    err_consent: 'Tick the consent box to continue.',
    err_too_big: 'The file is larger than 10 MB. Please choose a smaller photo.',
    err_type: 'Only JPG or PNG photos are supported.',
    err_generic: 'Something went wrong. Please try again.',
    err_speech: 'Speech is not supported in this browser.',
  },
};

/* ── Tiny helpers ───────────────────────────────────────────── */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => (
  { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const langKey = (l) => (l === 'mr' || l === 'hi' ? l : 'en');

/** UI string for the current language, with {placeholders} filled in. */
function t(key, vars) {
  const raw = (UI[currentLang] && UI[currentLang][key]) ?? UI.en[key] ?? key;
  return raw
    .replace(/\{team\}/g, BRAND.team)
    .replace(/\{event\}/g, BRAND.event)
    .replace(/\{(\w+)\}/g, (m, k) => (vars && k in vars ? String(vars[k]) : m));
}

/** Pick a localised field off an API object, falling back to English.
    The rules YAML has no title_hi/detail_hi, so Hindi falls back by design. */
const pick = (obj, base, k) => obj[`${base}_${k}`] || obj[`${base}_en`] || '';

const flagTitle = (f) => pick(f, 'title', currentLang);
const flagDetail = (f) => pick(f, 'detail', currentLang);
const flagTodo = (f) => pick(f, 'suggestion', currentLang);

const SEV_ICON = { serious: '⚠️', check: '🔍', info: 'ℹ️' };
const SEV_ORDER = { serious: 0, check: 1, info: 2 };

/* ── State ──────────────────────────────────────────────────── */
let currentLang = 'mr';
let lastResult = null;      // last /api/analyze payload
let lastResultLang = 'mr';  // language the AI summary + checklist came back in
let busy = false;
let previewUrl = null;

/* ── Screens ────────────────────────────────────────────────── */
function showScreen(name) {
  $$('.screen').forEach((s) => s.classList.toggle('is-active', s.id === `screen-${name}`));
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ── Language ───────────────────────────────────────────────── */
function applyLang(lang) {
  currentLang = langKey(lang);

  document.documentElement.lang = currentLang;
  document.title = currentLang === 'en'
    ? 'Satbara Saathi | सातबारा साथी'
    : 'सातबारा साथी | Satbara Saathi';

  const desc = $('meta[name="description"]');
  if (desc) desc.setAttribute('content', t('hero_sub'));

  $$('.lang-switch button').forEach((b) => {
    const on = b.dataset.lang === currentLang;
    b.classList.toggle('on', on);
    b.setAttribute('aria-pressed', String(on));
  });

  $$('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });

  syncConsentUI();
  hideError();

  // The whole result view is rebuilt from the payload, so switching language
  // re-translates the flags and checklist instantly — no re-upload needed.
  if (lastResult) renderResults(lastResult);
}

$$('.lang-switch button').forEach((b) => {
  b.addEventListener('click', () => applyLang(b.dataset.lang));
});

/* ── Consent gate ───────────────────────────────────────────── */
const consentBox = $('#consent');
const dropZone = $('#drop');

function consentGiven() { return consentBox.checked; }

function syncConsentUI() {
  const ok = consentGiven();
  dropZone.classList.toggle('is-locked', !ok);
  dropZone.setAttribute('aria-disabled', String(!ok));
  $('#drop-lock').hidden = ok;
}

consentBox.addEventListener('change', () => {
  syncConsentUI();
  if (consentGiven()) hideError();
});

/** Locked drop zone nudges the user toward the consent checkbox. */
function demandConsent() {
  showError(t('err_consent'));
  const row = $('#consent-row');
  row.classList.remove('nudge');
  void row.offsetWidth; // restart the animation
  row.classList.add('nudge');
  consentBox.focus();
}

/* ── Errors ─────────────────────────────────────────────────── */
function showError(msg) {
  const el = $('#err');
  el.textContent = msg;
  el.hidden = false;
}
function hideError() { $('#err').hidden = true; }

/* ── Toast ──────────────────────────────────────────────────── */
let toastTimer = null;
function toast(msg) {
  const el = $('#toast');
  el.textContent = msg;
  el.hidden = false;
  requestAnimationFrame(() => el.classList.add('is-on'));
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    el.classList.remove('is-on');
    setTimeout(() => { el.hidden = true; }, 260);
  }, 2200);
}

/* ── File picking ───────────────────────────────────────────── */
const fileInput = $('#file');
const cameraInput = $('#file-camera');

function openPicker(input) {
  if (!consentGiven()) { demandConsent(); return; }
  input.click();
}

$('#btn-pick').addEventListener('click', (e) => { e.stopPropagation(); openPicker(fileInput); });
$('#btn-camera').addEventListener('click', (e) => { e.stopPropagation(); openPicker(cameraInput); });
dropZone.addEventListener('click', (e) => {
  if (e.target.closest('button')) return;
  openPicker(fileInput);
});

fileInput.addEventListener('change', () => handleFile(fileInput.files[0]));
cameraInput.addEventListener('change', () => handleFile(cameraInput.files[0]));

// Drag & drop
['dragenter', 'dragover'].forEach((ev) => {
  dropZone.addEventListener(ev, (e) => {
    e.preventDefault();
    if (consentGiven()) dropZone.classList.add('is-over');
  });
});
['dragleave', 'dragend'].forEach((ev) => {
  dropZone.addEventListener(ev, () => dropZone.classList.remove('is-over'));
});
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('is-over');
  if (!consentGiven()) { demandConsent(); return; }
  const file = e.dataTransfer?.files?.[0];
  if (file) handleFile(file);
});

// Stop the browser from navigating away when a file misses the drop zone.
window.addEventListener('dragover', (e) => e.preventDefault());
window.addEventListener('drop', (e) => e.preventDefault());

/* ── Validation + preview ───────────────────────────────────── */
function validateFile(file) {
  if (!file.type.startsWith('image/')) return 'err_type';
  if (file.size > MAX_BYTES) return 'err_too_big';
  return null;
}

const humanSize = (bytes) =>
  bytes < 1024 * 1024
    ? `${Math.max(1, Math.round(bytes / 1024))} KB`
    : `${(bytes / (1024 * 1024)).toFixed(1)} MB`;

function showPreview(file) {
  const img = $('#preview');
  const ic = $('#preview-ic');
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  if (file.type.startsWith('image/')) {
    previewUrl = URL.createObjectURL(file);
    img.src = previewUrl;
    img.hidden = false;
    ic.hidden = true;
  } else {
    img.hidden = true;
    ic.hidden = false;
  }
  $('#doc-name').textContent = file.name || '—';
  $('#doc-size').textContent = humanSize(file.size);
}

/* ── Analysis stepper ───────────────────────────────────────── */
const STAGE_MS = 620;
let stageTimer = null;

function markStage(done) {
  $$('#steps li').forEach((li, i) => {
    li.classList.toggle('is-done', i < done);
    li.classList.toggle('is-active', i === done);
  });
}

function startStages() {
  let i = 0;
  markStage(0);
  clearInterval(stageTimer);
  stageTimer = setInterval(() => {
    i += 1;
    if (i >= 4) { clearInterval(stageTimer); markStage(4); return; }
    markStage(i);
  }, STAGE_MS);
}

function finishStages() {
  clearInterval(stageTimer);
  markStage(4);
}

/* ── Main flow ──────────────────────────────────────────────── */
async function handleFile(file) {
  if (!file || busy) return;
  fileInput.value = '';
  cameraInput.value = '';

  if (!consentGiven()) { demandConsent(); return; }

  const problem = validateFile(file);
  if (problem) { showError(t(problem)); return; }

  hideError();
  busy = true;
  showPreview(file);
  showScreen('analyzing');
  startStages();

  const startedAt = Date.now();
  const fd = new FormData();
  fd.append('file', file);
  fd.append('consent', 'true');
  fd.append('language', currentLang);
  fd.append('purpose', 'buying');

  try {
    const res = await fetch('/api/analyze', { method: 'POST', body: fd });
    if (!res.ok) {
      let detail = '';
      try { detail = (await res.json()).detail || ''; } catch { /* not JSON */ }
      throw new Error(detail || `HTTP ${res.status}`);
    }
    const data = await res.json();

    // Let the stepper finish so the process is legible, even on a fast server.
    const elapsed = Date.now() - startedAt;
    if (elapsed < 1400) await new Promise((r) => setTimeout(r, 1400 - elapsed));

    finishStages();
    await new Promise((r) => setTimeout(r, 420));

    lastResult = data;
    lastResultLang = currentLang;
    renderResults(data);
    showScreen('results');
    pushResultState();
  } catch (err) {
    clearInterval(stageTimer);
    showScreen('upload');
    const offline = err instanceof TypeError;
    showError(offline ? t('err_network') : (err.message || t('err_generic')));
  } finally {
    busy = false;
  }
}

/* ── Rendering ──────────────────────────────────────────────── */
function verdictLevel(flags, validationErrors) {
  if (flags.some((f) => f.severity === 'serious')) return 'serious';
  // A document we could not read properly is never "all clear".
  if (flags.some((f) => f.severity === 'check') || validationErrors.length) return 'check';
  return 'clear';
}

function renderVerdict(flags, validationErrors) {
  const level = verdictLevel(flags, validationErrors);
  const box = $('#verdict');
  box.classList.remove('is-serious', 'is-check', 'is-clear');
  box.classList.add(`is-${level}`);

  const serious = flags.filter((f) => f.severity === 'serious').length;
  const check = flags.filter((f) => f.severity === 'check').length;
  const info = flags.filter((f) => f.severity === 'info').length;

  const n = level === 'serious' ? serious : level === 'check' ? serious + check : 0;
  box.querySelector('.verdict-ic').textContent =
    level === 'serious' ? '⚠️' : level === 'check' ? '🔍' : '✅';
  $('#verdict-title').textContent = t(`v_${level}_t`);
  $('#verdict-body').textContent = t(`v_${level}_b`, { n });

  const counts = [];
  if (serious) counts.push(`<span class="count count-serious"><b>${serious}</b> ${esc(t('count_serious'))}</span>`);
  if (check) counts.push(`<span class="count count-check"><b>${check}</b> ${esc(t('count_check'))}</span>`);
  if (info) counts.push(`<span class="count count-info"><b>${info}</b> ${esc(t('count_info'))}</span>`);
  $('#counts').innerHTML = counts.join('');
}

function renderFlags(flags) {
  const box = $('#flags');
  $('#flags-count').textContent = String(flags.length);

  if (!flags.length) {
    box.innerHTML = `<p class="muted small">${esc(t('no_flags'))}</p>`;
    return;
  }

  const sorted = [...flags].sort(
    (a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9));

  box.innerHTML = sorted.map((f) => {
    const sev = ['serious', 'check', 'info'].includes(f.severity) ? f.severity : 'info';
    const detail = flagDetail(f).trim();
    const todo = flagTodo(f).trim();
    const evidence = Array.isArray(f.evidence) ? f.evidence : [];

    // Serious items start expanded; the rest stay collapsed to keep it scannable.
    const open = sev === 'serious' || sorted.length <= 2 ? ' open' : '';

    return `
      <details class="flag-card ${sev}"${open}>
        <summary>
          <span class="sev-chip ${sev}">${esc(t(`sev_${sev}`))}</span>
          <span class="flag-title">${esc(flagTitle(f))}</span>
          <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
               aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
        </summary>
        <div class="flag-body">
          ${detail ? `<p class="flag-detail">${esc(detail)}</p>` : ''}
          ${todo ? `<div class="flag-todo"><span class="lbl">${esc(t('todo'))}</span><p>${esc(todo)}</p></div>` : ''}
          ${evidence.length ? `<div class="flag-ev"><span class="lbl">${esc(t('evidence'))}</span>
            <ul>${evidence.map((e) => `<li>${esc(e)}</li>`).join('')}</ul></div>` : ''}
          <span class="flag-rule">${esc(t('rule_label'))} ${esc(f.rule_id)}</span>
        </div>
      </details>`;
  }).join('');
}

/* ── Checklist (progress is remembered per job) ─────────────── */
const CHECK_KEY = (jobId) => `satbara.checklist.${jobId}`;

function loadChecked(jobId) {
  try { return JSON.parse(localStorage.getItem(CHECK_KEY(jobId)) || '[]'); } catch { return []; }
}
function saveChecked(jobId, ids) {
  try { localStorage.setItem(CHECK_KEY(jobId), JSON.stringify(ids)); } catch { /* private mode */ }
}

function renderChecklist(items, jobId) {
  const box = $('#checklist');
  $('#check-count').textContent = String(items.length);

  if (!items.length) {
    box.innerHTML = '';
    $('#check-progress').hidden = true;
    return;
  }

  const checked = loadChecked(jobId);
  const extIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
    stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M14 4h6v6"/><path d="M20 4 11 13"/>
    <path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>`;

  box.innerHTML = items.map((item, i) => {
    const id = String(item.step ?? i + 1);
    const isDone = checked.includes(id);
    const link = item.url
      ? `<a class="check-link" href="${esc(item.url)}" target="_blank" rel="noopener noreferrer"
            aria-label="${esc(item.title)}">${extIcon}</a>`
      : '';
    return `
      <li class="check-item${isDone ? ' is-done' : ''}">
        <label>
          <input type="checkbox" data-step="${esc(id)}"${isDone ? ' checked' : ''}>
          <span class="check-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"
            aria-hidden="true"><path d="m5 13 4.5 4.5L19 7"/></svg></span>
          <span class="check-num" aria-hidden="true">${esc(id)}</span>
          <span class="check-title">${esc(item.title)}</span>
        </label>
        ${link}
      </li>`;
  }).join('');

  box.onchange = (e) => {
    const input = e.target.closest('input[type=checkbox]');
    if (!input) return;
    const li = input.closest('.check-item');
    li.classList.toggle('is-done', input.checked);
    const done = Array.from(box.querySelectorAll('input:checked')).map((el) => el.dataset.step);
    saveChecked(jobId, done);
    updateProgress(items.length, done.length);
  };

  $('#check-progress').hidden = false;
  updateProgress(items.length, checked.length);
}

function updateProgress(total, done) {
  $('#check-progress').querySelector('i').style.width =
    total ? `${Math.round((done / total) * 100)}%` : '0';
  $('#check-count').textContent = t('done_count', { done, total });
}

/* ── Photo quality ──────────────────────────────────────────── */
function gradeOf(score) {
  if (score >= 0.7) return { cls: '', label: 'q_good' };
  if (score >= 0.45) return { cls: 'warn', label: 'q_fair' };
  return { cls: 'bad', label: 'q_poor' };
}

function renderQuality(quality) {
  const card = $('#quality-card');
  if (!quality) { card.hidden = true; return; }
  card.hidden = false;

  const rows = [
    ['q_blur', quality.blur_score],
    ['q_bright', quality.brightness_score],
    ['q_texture', quality.texture_score],
  ];
  const overall = quality.overall_score;
  const grade = gradeOf(overall);
  $('#quality-chip').textContent = t(grade.label);

  $('#quality-bars').innerHTML = rows.map(([key, val]) => {
    const v = Math.max(0, Math.min(1, Number(val) || 0));
    const g = gradeOf(v);
    return `
      <div class="bar-row">
        <span class="bar-label">${esc(t(key))}</span>
        <span class="bar-val">${Math.round(v * 100)}%</span>
        <span class="bar"><i class="${g.cls}" style="width:${Math.round(v * 100)}%"></i></span>
      </div>`;
  }).join('') + `
      <div class="bar-row" style="margin-top:.35rem">
        <span class="bar-label"><strong>${esc(t('q_overall'))}</strong></span>
        <span class="bar-val">${Math.round((Number(overall) || 0) * 100)}%</span>
        <span class="bar"><i class="${grade.cls}" style="width:${Math.round((Number(overall) || 0) * 100)}%"></i></span>
      </div>`;

  const warnings = Array.isArray(quality.warnings) ? quality.warnings : [];
  const warnBox = $('#quality-warnings');
  warnBox.innerHTML = warnings.length
    ? warnings.map((w) => `<li>${esc(w)}</li>`).join('')
    : `<li class="ok">${esc(t('quality_ok'))}</li>`;
}

/* ── Validation errors ──────────────────────────────────────── */
function renderErrors(errors) {
  const card = $('#errors-card');
  const list = Array.isArray(errors) ? errors : [];
  card.hidden = list.length === 0;
  $('#errors').innerHTML = list.map((e) => `<li>${esc(e)}</li>`).join('');
}

/* ── Whole result view ──────────────────────────────────────── */
function renderResults(data) {
  const flags = Array.isArray(data.flags) ? data.flags : [];
  const errors = Array.isArray(data.validation_errors) ? data.validation_errors : [];
  const checklist = Array.isArray(data.checklist) ? data.checklist : [];

  $('#res-job').textContent = data.job_id ? `#${data.job_id}` : '';

  renderVerdict(flags, errors);
  renderFlags(flags);
  renderChecklist(checklist, data.job_id || 'anon');
  renderQuality(data.quality);
  renderErrors(errors);

  const summaryEl = $('#summary');
  summaryEl.textContent = (data.explanation && data.explanation.summary) || t('no_flags');

  // The summary and checklist are generated server-side in the language that
  // was requested, so say so when the reader has since switched language.
  const note = $('#lang-note');
  if (lastResultLang !== currentLang) {
    note.textContent = t('lang_note', { lang: t(`lang_${lastResultLang}`) });
    note.hidden = false;
  } else {
    note.hidden = true;
  }

  $('#disclaimer').textContent = data.disclaimer || '';
  stopSpeaking();

  const fb = $('#fb');
  fb.classList.remove('is-answered');
  fb.querySelector('.thanks')?.remove();
}

/* ── Text to speech (browser-native: works offline, no API key) ── */
const canSpeak = 'speechSynthesis' in window;
let speaking = false;

function speechText() {
  if (!lastResult) return '';
  const parts = [];
  const summary = lastResult.explanation && lastResult.explanation.summary;
  if (summary) parts.push(summary);
  (lastResult.flags || []).forEach((f) => {
    const title = flagTitle(f);
    const detail = flagDetail(f).trim();
    parts.push(detail ? `${title}. ${detail}` : title);
  });
  return parts.join('. ');
}

function setListenLabel(on) {
  const btn = $('#btn-listen');
  btn.querySelector('span').textContent = on ? t('listen_stop') : t('listen');
  btn.setAttribute('aria-pressed', String(on));
}

function stopSpeaking() {
  if (canSpeak) speechSynthesis.cancel();
  speaking = false;
  setListenLabel(false);
}

function speakAloud() {
  if (!canSpeak) { showError(t('err_speech')); return; }
  const text = speechText();
  if (!text) return;
  const ut = new SpeechSynthesisUtterance(text);
  ut.lang = currentLang === 'mr' ? 'mr-IN' : currentLang === 'hi' ? 'hi-IN' : 'en-US';
  ut.rate = 0.95;
  ut.onend = () => { speaking = false; setListenLabel(false); };
  ut.onerror = () => { speaking = false; setListenLabel(false); };
  speechSynthesis.cancel();
  speechSynthesis.speak(ut);
  speaking = true;
  setListenLabel(true);
}

$('#btn-listen').addEventListener('click', () => {
  if (speaking) stopSpeaking(); else speakAloud();
});

/* ── Copy a plain-text report ───────────────────────────────── */
function reportText() {
  if (!lastResult) return '';
  const flags = lastResult.flags || [];
  const lines = [
    `${t('brand')} — ${t('res_title')}`,
    '',
    `${t('verdict_kicker')}: ${$('#verdict-title').textContent}`,
    `${t('sec_summary')}: ${$('#summary').textContent}`,
  ];
  if (flags.length) {
    lines.push('', `${t('sec_flags')}:`);
    flags.forEach((f) => {
      lines.push(`• [${t(`sev_${f.severity}`)}] ${flagTitle(f)}`);
      const detail = flagDetail(f).trim();
      if (detail) lines.push(`  ${detail}`);
      const todo = flagTodo(f).trim();
      if (todo) lines.push(`  ${t('todo')}: ${todo}`);
    });
  }
  const steps = lastResult.checklist || [];
  if (steps.length) {
    lines.push('', `${t('sec_checklist')}:`);
    steps.forEach((s, i) => lines.push(`${s.step ?? i + 1}. ${s.title}`));
  }
  lines.push('', lastResult.disclaimer || '', 'https://mahabhulekh.maharashtra.gov.in');
  return lines.join('\n');
}

$('#btn-copy').addEventListener('click', async () => {
  const text = reportText();
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    toast(t('copied'));
  } catch {
    // Fallback for non-secure origins, where the Clipboard API is unavailable.
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-1000px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); toast(t('copied')); }
    catch { showError(t('err_generic')); }
    ta.remove();
  }
});

$('#btn-print').addEventListener('click', () => window.print());

/* ── Feedback ───────────────────────────────────────────────── */
function answerFeedback(positive) {
  const fb = $('#fb');
  if (fb.classList.contains('is-answered')) return;
  fb.classList.add('is-answered');
  const span = document.createElement('span');
  span.className = 'thanks';
  span.textContent = t('fb_thanks');
  fb.appendChild(span);
  // No backend endpoint for this yet — kept local, nothing leaves the device.
  console.info('[satbara] feedback', positive ? 'clear' : 'unclear');
}

$('#fb-yes').addEventListener('click', () => answerFeedback(true));
$('#fb-no').addEventListener('click', () => answerFeedback(false));

/* ── Start over ─────────────────────────────────────────────── */
function resetToUpload() {
  stopSpeaking();
  lastResult = null;
  renderChecklist([], 'anon');
  $('#flags').innerHTML = '';
  $('#errors-card').hidden = true;
  $('#quality-card').hidden = true;
  showScreen('upload');
}

$('#btn-new').addEventListener('click', () => {
  resetToUpload();
  try { history.replaceState(null, '', location.pathname); } catch { /* file:// */ }
});

$('#brand-home').addEventListener('click', () => {
  resetToUpload();
  try { history.replaceState(null, '', location.pathname); } catch { /* file:// */ }
});

/* Let the browser Back button return to the upload screen. */
function pushResultState() {
  try { history.pushState({ screen: 'results' }, '', '#results'); } catch { /* file:// */ }
}
window.addEventListener('popstate', () => {
  if (lastResult && $('#screen-results').classList.contains('is-active')) resetToUpload();
});

/* ── Init ───────────────────────────────────────────────────── */
applyLang('mr');
