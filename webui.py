# TikSaver web pages, inlined so the deploy package stays flat
# (no templates folder needed): home page + About/Privacy/DMCA.
INDEX_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TikSaver — TikTok, Instagram & Facebook Video Downloader (No Watermark)</title>
<meta name="description" content="TikSaver is a free video downloader. Paste a TikTok, Instagram or Facebook link and save the video in MP4 without watermark, or get the audio as MP3. No app install, no account needed.">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, "Segoe UI", Roboto, "Noto Nastaliq Urdu", Arial, sans-serif; background: #f6f7fb; color: #1c1e26; }
  body.ur { direction: rtl; }
  header { background: linear-gradient(120deg, #10121f, #23263e 55%, #3a1042); color: #fff; padding: 20px 16px 38px; text-align: center; position: relative; }
  .langbar { position: absolute; top: 12px; right: 14px; font-size: 13px; }
  body.ur .langbar { right: auto; left: 14px; }
  .langbar button { background: rgba(255,255,255,.14); color: #fff; border: 1px solid rgba(255,255,255,.35); padding: 5px 10px; border-radius: 999px; font-size: 13px; font-weight: 700; cursor: pointer; }
  .langbar button.on { background: #fe2c55; border-color: #fe2c55; }
  .brand { display: inline-flex; align-items: center; gap: 10px; }
  .mark { width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #25f4ee, #fe2c55); display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(0,0,0,.35); }
  .logo { font-size: 30px; font-weight: 800; letter-spacing: .5px; }
  .logo span { color: #25f4ee; }
  .logo b { color: #fe2c55; font-weight: 800; }
  header p { opacity: .88; margin-top: 8px; font-size: 15px; line-height: 1.5; }
  .chips { margin-top: 12px; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
  .chip { background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25); padding: 5px 12px; border-radius: 999px; font-size: 13px; font-weight: 600; }
  .counter { margin-top: 12px; display: inline-block; background: rgba(18,183,106,.18); border: 1px solid rgba(18,183,106,.55); color: #b9ffd9; padding: 6px 14px; border-radius: 999px; font-size: 14px; font-weight: 700; }
  .card { background: #fff; max-width: 640px; margin: -18px auto 18px; border-radius: 14px; box-shadow: 0 6px 24px rgba(20,22,40,.10); padding: 18px 16px 20px; width: calc(100% - 24px); }
  .row { display: flex; gap: 8px; }
  input[type=text] { flex: 1; padding: 13px 12px; font-size: 16px; border: 2px solid #e3e5ef; border-radius: 10px; outline: none; min-width: 0; direction: ltr; text-align: left; }
  input[type=text]:focus { border-color: #fe2c55; }
  button { border: 0; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; padding: 13px 16px; }
  .paste { background: #eceef6; color: #25273a; }
  .go { background: #fe2c55; color: #fff; width: 100%; margin-top: 10px; padding: 15px; font-size: 17px; }
  .go:disabled { opacity: .55; }
  .msg { margin-top: 12px; font-size: 15px; text-align: center; min-height: 20px; }
  .msg.err { color: #d1113c; }
  #result { display: none; margin-top: 14px; text-align: center; }
  #result img { max-width: 220px; width: 60%; border-radius: 10px; }
  #result h3 { font-size: 16px; margin: 10px 0 4px; }
  #result .meta { color: #666; font-size: 14px; margin-bottom: 12px; }
  .dl { display: block; background: #12b76a; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 10px; font-size: 16px; margin-top: 8px; }
  .dlrow { display: flex; gap: 8px; margin-top: 8px; }
  .dlrow .dl { flex: 1; margin-top: 0; }
  .dl.sd { background: #475069; }
  .dl.mp3 { background: #7c3aed; }
  section { max-width: 640px; margin: 0 auto 18px; padding: 0 16px; }
  section h2 { font-size: 19px; margin-bottom: 10px; }
  .steps { background: #fff; border-radius: 14px; padding: 16px 18px; box-shadow: 0 3px 14px rgba(20,22,40,.06); }
  .steps li { margin: 8px 0 8px 18px; font-size: 15px; line-height: 1.5; }
  body.ur .steps li { margin: 8px 18px 8px 0; }
  .small { color: #666; font-size: 13px; line-height: 1.6; }
  footer { text-align: center; color: #888; font-size: 13px; padding: 14px 10px 26px; line-height: 2; }
  footer a { color: #666; font-weight: 600; text-decoration: none; margin: 0 8px; }
  footer a:hover { color: #fe2c55; }
</style>
</head>
<body>
<header>
  <div class="langbar">
    <button id="langEn" class="on" type="button">EN</button>
    <button id="langUr" type="button">اردو</button>
  </div>
  <div class="brand">
    <span class="mark"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 3v10m0 0l-4.2-4.2M12 13l4.2-4.2" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 17v2.2A1.8 1.8 0 0 0 5.8 21h12.4a1.8 1.8 0 0 0 1.8-1.8V17" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg></span>
    <span class="logo">Tik<span>Saver</span><b>.</b></span>
  </div>
  <p data-i18n="tagline">Download TikTok, Instagram &amp; Facebook videos without watermark — free, fast, no account needed.</p>
  <div class="chips"><span class="chip">🎵 TikTok</span><span class="chip">📸 Instagram</span><span class="chip">📘 Facebook</span><span class="chip">🎧 MP3</span></div>
  <div><span class="counter">🔥 %%COUNT%% <span data-i18n="counter">videos downloaded so far</span></span></div>
</header>

<div class="card">
  <div class="row">
    <input type="text" id="link" data-i18n-ph="placeholder" placeholder="Paste a TikTok, Instagram or Facebook link here…" autocomplete="off">
    <button class="paste" id="pasteBtn" type="button" data-i18n="paste">Paste</button>
  </div>
  <button class="go" id="goBtn" type="button" data-i18n="go">Get Video</button>
  <div class="msg" id="msg"></div>
  <div id="result">
    <img id="thumb" alt="Video thumbnail">
    <h3 id="rtitle"></h3>
    <div class="meta" id="rmeta"></div>
    <a class="dl" id="dlHd" href="#" data-i18n="dlhd">⬇ Download MP4 — HD (No Watermark)</a>
    <div class="dlrow">
      <a class="dl sd" id="dlSd" href="#" data-i18n="dlsd">⬇ MP4 — SD (small file)</a>
      <a class="dl mp3" id="dlMp3" href="#" data-i18n="dlmp3">🎵 MP3 (audio only)</a>
    </div>
  </div>
</div>

<section>
  <h2 data-i18n="howto">How to download a video</h2>
  <div class="steps">
    <ol>
      <li data-i18n="step1">Open the app (TikTok, Instagram or Facebook) and find the video you want to save.</li>
      <li data-i18n="step2">Tap <b>Share</b> and then <b>Copy link</b>.</li>
      <li data-i18n="step3">Paste the link above and tap <b>Get Video</b> — then choose HD, SD or MP3.</li>
    </ol>
  </div>
</section>

<section>
  <p class="small" data-i18n="note">TikSaver is a free tool for saving videos for personal use. Please respect the rights of the original creators — only download videos you have permission to save, and do not re-upload other people's work as your own. TikSaver is not affiliated with TikTok, ByteDance, Instagram, Facebook or Meta.</p>
</section>

<footer>
  <a href="/about" data-i18n="about">About</a>·<a href="/privacy" data-i18n="privacy">Privacy Policy</a>·<a href="/dmca">DMCA</a>
  <br>© 2026 TikSaver — <span data-i18n="foot">Made for personal use.</span>
</footer>

<script>
  var I18N = {
    en: {
      tagline: "Download TikTok, Instagram & Facebook videos without watermark — free, fast, no account needed.",
      counter: "videos downloaded so far",
      placeholder: "Paste a TikTok, Instagram or Facebook link here…",
      paste: "Paste", go: "Get Video",
      howto: "How to download a video",
      step1: "Open the app (TikTok, Instagram or Facebook) and find the video you want to save.",
      step2: "Tap Share and then Copy link.",
      step3: "Paste the link above and tap Get Video — then choose HD, SD or MP3.",
      note: "TikSaver is a free tool for saving videos for personal use. Please respect the rights of the original creators — only download videos you have permission to save, and do not re-upload other people's work as your own. TikSaver is not affiliated with TikTok, ByteDance, Instagram, Facebook or Meta.",
      about: "About", privacy: "Privacy Policy", foot: "Made for personal use.",
      dlhd: "⬇ Download MP4 — HD (No Watermark)", dlsd: "⬇ MP4 — SD (small file)", dlmp3: "🎵 MP3 (audio only)",
      fetching: "Fetching your video… please wait a few seconds.", ready: "Your video is ready:",
      errlink: "Please paste a valid TikTok, Instagram or Facebook link first.",
      errnet: "Network problem. Please try again.", seconds: "seconds"
    },
    ur: {
      tagline: "TikTok، Instagram اور Facebook ویڈیوز واٹر مارک کے بغیر ڈاؤن لوڈ کریں — مفت، تیز، اکاؤنٹ کی ضرورت نہیں۔",
      counter: "ویڈیوز اب تک ڈاؤن لوڈ ہو چکیں",
      placeholder: "یہاں TikTok، Instagram یا Facebook کا لنک لگائیں…",
      paste: "چسپاں", go: "ویڈیو حاصل کریں",
      howto: "ویڈیو کیسے ڈاؤن لوڈ کریں",
      step1: "ایپ (TikTok، Instagram یا Facebook) کھولیں اور جو ویڈیو محفوظ کرنی ہے وہ تلاش کریں۔",
      step2: "Share دبائیں اور پھر Copy link دبائیں۔",
      step3: "لنک اوپر لگائیں اور «ویڈیو حاصل کریں» دبائیں — پھر HD، SD یا MP3 منتخب کریں۔",
      note: "TikSaver ذاتی استعمال کے لیے ویڈیوز محفوظ کرنے کا مفت ذریعہ ہے۔ براہ کرم اصل بنانے والوں کے حقوق کا احترام کریں — صرف وہی ویڈیوز ڈاؤن لوڈ کریں جن کی آپ کو اجازت ہو، اور دوسروں کے کام کو اپنا کہہ کر دوبارہ اپ لوڈ نہ کریں۔ TikSaver کا TikTok، ByteDance، Instagram، Facebook یا Meta سے کوئی تعلق نہیں۔",
      about: "ہمارے بارے میں", privacy: "پرائیویسی پالیسی", foot: "ذاتی استعمال کے لیے بنایا گیا۔",
      dlhd: "⬇ MP4 ڈاؤن لوڈ — HD (واٹر مارک کے بغیر)", dlsd: "⬇ MP4 — SD (چھوٹی فائل)", dlmp3: "🎵 MP3 (صرف آواز)",
      fetching: "آپ کی ویڈیو لائی جا رہی ہے… چند سیکنڈ انتظار کریں۔", ready: "آپ کی ویڈیو تیار ہے:",
      errlink: "پہلے درست لنک لگائیں (TikTok، Instagram یا Facebook)۔",
      errnet: "نیٹ ورک مسئلہ۔ دوبارہ کوشش کریں۔", seconds: "سیکنڈ"
    }
  };
  var lang = 'en';
  try { lang = localStorage.getItem('ts_lang') || 'en'; } catch (e) {}
  function applyLang(l) {
    lang = l;
    try { localStorage.setItem('ts_lang', l); } catch (e) {}
    document.body.classList.toggle('ur', l === 'ur');
    document.getElementById('langEn').classList.toggle('on', l === 'en');
    document.getElementById('langUr').classList.toggle('on', l === 'ur');
    var d = I18N[l];
    var els = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < els.length; i++) {
      var k = els[i].getAttribute('data-i18n');
      if (d[k]) els[i].textContent = d[k];
    }
    var ph = document.querySelectorAll('[data-i18n-ph]');
    for (var j = 0; j < ph.length; j++) {
      var k2 = ph[j].getAttribute('data-i18n-ph');
      if (d[k2]) ph[j].setAttribute('placeholder', d[k2]);
    }
  }
  document.getElementById('langEn').addEventListener('click', function () { applyLang('en'); });
  document.getElementById('langUr').addEventListener('click', function () { applyLang('ur'); });

  var linkEl = document.getElementById('link');
  var msgEl = document.getElementById('msg');
  var goBtn = document.getElementById('goBtn');
  var resultEl = document.getElementById('result');

  document.getElementById('pasteBtn').addEventListener('click', function () {
    if (navigator.clipboard && navigator.clipboard.readText) {
      navigator.clipboard.readText().then(function (t) {
        if (t) linkEl.value = t;
      }).catch(function () { linkEl.focus(); });
    } else { linkEl.focus(); }
  });

  goBtn.addEventListener('click', function () {
    var url = linkEl.value.trim();
    var d = I18N[lang];
    msgEl.className = 'msg';
    resultEl.style.display = 'none';
    if (!url || !/(tiktok\.com|instagram\.com|facebook\.com|fb\.watch)/.test(url)) {
      msgEl.className = 'msg err';
      msgEl.textContent = d.errlink;
      return;
    }
    goBtn.disabled = true;
    msgEl.textContent = d.fetching;
    fetch('/api/resolve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    }).then(function (r) { return r.json(); }).then(function (res) {
      goBtn.disabled = false;
      if (!res.ok) {
        msgEl.className = 'msg err';
        msgEl.textContent = res.error || 'Something went wrong.';
        return;
      }
      msgEl.textContent = d.ready;
      document.getElementById('rtitle').textContent = res.title || 'Video';
      document.getElementById('rmeta').textContent =
        (res.platform ? res.platform + '  ·  ' : '') +
        (res.uploader ? '@' + res.uploader + '  ·  ' : '') +
        (res.duration ? Math.round(res.duration) + ' ' + d.seconds : '');
      var img = document.getElementById('thumb');
      if (res.thumbnail) { img.src = res.thumbnail; img.style.display = ''; }
      else { img.style.display = 'none'; }
      document.getElementById('dlHd').href = res.download_hd || res.download;
      document.getElementById('dlSd').href = res.download_sd || res.download;
      document.getElementById('dlMp3').href = res.mp3;
      resultEl.style.display = 'block';
    }).catch(function () {
      goBtn.disabled = false;
      msgEl.className = 'msg err';
      msgEl.textContent = d.errnet;
    });
  });
  applyLang(lang);
</script>
</body>
</html>
'''

_PAGE_STYLE = '''
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif; background: #f6f7fb; color: #1c1e26; }
  header { background: linear-gradient(120deg, #10121f, #23263e 55%, #3a1042); color: #fff; padding: 22px 16px; text-align: center; }
  .logo { font-size: 24px; font-weight: 800; }
  .logo span { color: #25f4ee; } .logo b { color: #fe2c55; }
  main { max-width: 680px; margin: 22px auto; background: #fff; border-radius: 14px; box-shadow: 0 3px 14px rgba(20,22,40,.06); padding: 24px 22px; width: calc(100% - 24px); }
  h1 { font-size: 22px; margin-bottom: 14px; }
  p, li { font-size: 15px; line-height: 1.65; margin-bottom: 10px; }
  ul { margin-left: 20px; }
  a { color: #d1113c; font-weight: 600; text-decoration: none; }
  .back { display: inline-block; margin-top: 10px; }
  footer { text-align: center; color: #888; font-size: 13px; padding: 10px 10px 26px; }
</style>
'''

def _page(title, body_html):
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{title} — TikSaver</title>' + _PAGE_STYLE + '</head><body>'
            '<header><div class="logo">Tik<span>Saver</span><b>.</b></div></header>'
            f'<main>{body_html}<a class="back" href="/">← Back to TikSaver</a></main>'
            '<footer>© 2026 TikSaver</footer></body></html>')

ABOUT_HTML = _page("About", '''
<h1>About TikSaver</h1>
<p>TikSaver is a free online tool that helps you save videos from TikTok, Instagram and Facebook for personal, offline viewing. Paste a video link, and TikSaver fetches the video so you can download it as an MP4 file (in HD or SD quality) or save just the audio as an MP3.</p>
<p>There is no app to install and no account to create — the tool works entirely in your browser.</p>
<p>TikSaver is made for personal use only. Videos belong to their original creators; please respect their rights and your local laws, and never re-upload someone else's work as your own.</p>
<p>TikSaver is an independent tool and is <b>not affiliated with</b> TikTok, ByteDance, Instagram, Facebook or Meta.</p>
<p>Questions or feedback: <a href="mailto:teamk5317@gmail.com">teamk5317@gmail.com</a></p>
''')

PRIVACY_HTML = _page("Privacy Policy", '''
<h1>Privacy Policy</h1>
<p><i>Last updated: November 2026</i></p>
<p>TikSaver is built to need as little of your information as possible:</p>
<ul>
  <li><b>No accounts.</b> You never sign up or log in, and we never ask for your name, email or password.</li>
  <li><b>Links are processed on the fly.</b> When you paste a video link, our server fetches that video and sends it to you. Video files are not stored on our server after your download finishes.</li>
  <li><b>A simple counter.</b> We keep one anonymous number — how many downloads have been served in total — shown on the home page. It is not linked to you in any way.</li>
  <li><b>Server logs.</b> Like almost every website, our hosting provider keeps short technical logs (such as IP address and browser type) for security and abuse prevention.</li>
  <li><b>Cookies.</b> TikSaver itself does not set tracking cookies. The site remembers only your language choice (English/Urdu) in your own browser.</li>
  <li><b>Advertising.</b> If ads are added in the future, the advertising partner's cookies and policy will apply, and this page will be updated before that happens.</li>
</ul>
<p>Questions about privacy: <a href="mailto:teamk5317@gmail.com">teamk5317@gmail.com</a></p>
''')

DMCA_HTML = _page("DMCA & Copyright", '''
<h1>DMCA &amp; Copyright</h1>
<p>TikSaver respects the intellectual property rights of creators and expects its users to do the same. TikSaver is a tool that fetches publicly available videos at a user's request for personal use; it does not host, store or redistribute videos.</p>
<p>If you are a copyright owner (or their authorised agent) and you believe content accessible through TikSaver infringes your rights, please email us with:</p>
<ul>
  <li>Your full name and contact details</li>
  <li>The exact link(s) involved</li>
  <li>Proof that you own the rights, or are authorised to act for the owner</li>
</ul>
<p>Send your notice to: <a href="mailto:teamk5317@gmail.com">teamk5317@gmail.com</a></p>
<p>Valid notices are reviewed promptly, and we will take appropriate action, which can include blocking the specific link or source from being processed by TikSaver.</p>
<p>Users are reminded: only download videos you have the right to save, and never present other people's work as your own.</p>
''')
