# Auto-generated: the TikSaver home page, inlined so the deploy
# package is flat files only (no templates folder needed).
INDEX_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TikSaver — Download TikTok Videos Without Watermark</title>
<meta name="description" content="TikSaver is a free TikTok video downloader. Paste a TikTok link and save the video in MP4, without watermark. No app install, no account needed.">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif; background: #f6f7fb; color: #1c1e26; }
  header { background: linear-gradient(120deg, #161823, #25273a); color: #fff; padding: 18px 16px 34px; text-align: center; }
  .logo { font-size: 28px; font-weight: 800; letter-spacing: .5px; }
  .logo span { color: #25f4ee; }
  .logo b { color: #fe2c55; font-weight: 800; }
  header p { opacity: .85; margin-top: 6px; font-size: 15px; }
  .card { background: #fff; max-width: 640px; margin: -18px auto 18px; border-radius: 14px; box-shadow: 0 6px 24px rgba(20,22,40,.10); padding: 18px 16px 20px; width: calc(100% - 24px); }
  .row { display: flex; gap: 8px; }
  input[type=text] { flex: 1; padding: 13px 12px; font-size: 16px; border: 2px solid #e3e5ef; border-radius: 10px; outline: none; min-width: 0; }
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
  .dl { display: inline-block; background: #12b76a; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 10px; font-size: 16px; }
  section { max-width: 640px; margin: 0 auto 18px; padding: 0 16px; width: calc(100% - 0px); }
  section h2 { font-size: 19px; margin-bottom: 10px; }
  .steps { background: #fff; border-radius: 14px; padding: 16px 18px; box-shadow: 0 3px 14px rgba(20,22,40,.06); }
  .steps li { margin: 8px 0 8px 18px; font-size: 15px; line-height: 1.5; }
  .small { color: #666; font-size: 13px; line-height: 1.6; }
  footer { text-align: center; color: #888; font-size: 13px; padding: 14px 10px 26px; }
</style>
</head>
<body>
<header>
  <div class="logo">Tik<span>Saver</span><b>.</b></div>
  <p>Download TikTok videos without watermark — free, fast, no account needed.</p>
</header>

<div class="card">
  <div class="row">
    <input type="text" id="link" placeholder="Paste TikTok link here…" autocomplete="off">
    <button class="paste" id="pasteBtn" type="button">Paste</button>
  </div>
  <button class="go" id="goBtn" type="button">Download Video</button>
  <div class="msg" id="msg"></div>
  <div id="result">
    <img id="thumb" alt="Video thumbnail">
    <h3 id="rtitle"></h3>
    <div class="meta" id="rmeta"></div>
    <a class="dl" id="dlBtn" href="#">⬇ Download MP4 (No Watermark)</a>
  </div>
</div>

<section>
  <h2>How to download a TikTok video</h2>
  <div class="steps">
    <ol>
      <li>Open the TikTok app and find the video you want to save.</li>
      <li>Tap <b>Share</b> and then <b>Copy link</b>.</li>
      <li>Paste the link above and tap <b>Download Video</b> — your MP4 saves without the watermark.</li>
    </ol>
  </div>
</section>

<section>
  <p class="small">TikSaver is a free tool for saving TikTok videos for personal use. Please respect the rights of the original creators — only download videos you have permission to save, and do not re-upload other people's work as your own. TikSaver is not affiliated with TikTok or ByteDance.</p>
</section>

<footer>© 2026 TikSaver — Made for personal use.</footer>

<script>
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
    msgEl.className = 'msg';
    resultEl.style.display = 'none';
    if (!url || url.indexOf('tiktok.com') === -1) {
      msgEl.className = 'msg err';
      msgEl.textContent = 'Please paste a valid TikTok link first.';
      return;
    }
    goBtn.disabled = true;
    msgEl.textContent = 'Fetching your video… please wait a few seconds.';
    fetch('/api/resolve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    }).then(function (r) { return r.json(); }).then(function (d) {
      goBtn.disabled = false;
      if (!d.ok) {
        msgEl.className = 'msg err';
        msgEl.textContent = d.error || 'Something went wrong.';
        return;
      }
      msgEl.textContent = 'Your video is ready:';
      document.getElementById('rtitle').textContent = d.title || 'TikTok video';
      document.getElementById('rmeta').textContent =
        (d.uploader ? '@' + d.uploader + '  ·  ' : '') +
        (d.duration ? Math.round(d.duration) + ' seconds' : '');
      var img = document.getElementById('thumb');
      if (d.thumbnail) { img.src = d.thumbnail; img.style.display = ''; }
      else { img.style.display = 'none'; }
      document.getElementById('dlBtn').href = d.download;
      resultEl.style.display = 'block';
    }).catch(function () {
      goBtn.disabled = false;
      msgEl.className = 'msg err';
      msgEl.textContent = 'Network problem. Please try again.';
    });
  });
</script>
</body>
</html>
'''
