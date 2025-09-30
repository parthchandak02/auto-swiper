(() => {
  const byId = (id) => document.getElementById(id);
  const repoMeta = detectRepo();
  const yearEl = byId('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  if (repoMeta) {
    const { repoUrl, releasesUrl, actionsUrl, owner, repo } = repoMeta;
    const repoLink = byId('repoLink');
    const releasesLink = byId('releasesLink');
    const actionsLink = byId('actionsLink');
    if (repoLink) repoLink.href = repoUrl;
    if (releasesLink) releasesLink.href = releasesUrl;
    if (actionsLink) actionsLink.href = actionsUrl;
    fetchLatestRelease(owner, repo)
      .then(applyRelease)
      .catch(() => setFallbackLinks(releasesUrl));
  }

  function detectRepo() {
    const host = location.hostname;
    const isPages = host.endsWith('github.io');
    if (!isPages) return null;
    const owner = host.split('.')[0];
    const pathParts = location.pathname.replace(/^\/+|\/+$/g, '').split('/');
    const repo = pathParts[0] || '';
    if (!owner || !repo) return null;
    const repoUrl = `https://github.com/${owner}/${repo}`;
    return {
      owner,
      repo,
      repoUrl,
      releasesUrl: `${repoUrl}/releases/latest`,
      actionsUrl: `${repoUrl}/actions`,
    };
  }

  async function fetchLatestRelease(owner, repo) {
    const url = `https://api.github.com/repos/${owner}/${repo}/releases/latest`;
    const res = await fetch(url, { headers: { Accept: 'application/vnd.github+json' } });
    if (!res.ok) throw new Error('Failed to fetch latest release');
    return res.json();
  }

  function applyRelease(release) {
    const info = byId('releaseInfo');
    if (info) info.textContent = `Latest: ${release.name || release.tag_name || 'untagged'}`;
    const assets = Array.isArray(release.assets) ? release.assets : [];
    const links = mapAssets(assets);
    wireBtn('btnWindows', links.windows);
    wireBtn('btnMac', links.macos);
    wireBtn('btnLinux', links.linux);
  }

  function setFallbackLinks(releasesUrl) {
    const info = byId('releaseInfo');
    if (info) info.textContent = 'Visit Releases to download builds.';
    ['btnWindows', 'btnMac', 'btnLinux'].forEach((id) => wireBtn(id, releasesUrl));
  }

  function wireBtn(id, href) {
    const el = byId(id);
    if (!el) return;
    if (href) {
      el.classList.remove('disabled');
      el.setAttribute('href', href);
      el.setAttribute('aria-disabled', 'false');
    }
  }

  function mapAssets(assets) {
    const lower = (s) => (s || '').toLowerCase();
    const find = (pred) => assets.find((a) => pred(lower(a.name)) || pred(lower(a.browser_download_url)));
    const windows = find((s) => s.includes('windows') || s.endsWith('.exe'));
    const macos = find((s) => s.includes('macos') || s.includes('darwin') || s.includes('osx') || s.endsWith('.zip'));
    const linux = find((s) => s.includes('linux') || (!/[.][a-z0-9]+$/.test(s))); // bare binary
    return {
      windows: windows ? windows.browser_download_url : null,
      macos: macos ? macos.browser_download_url : null,
      linux: linux ? linux.browser_download_url : null,
    };
  }
})();

