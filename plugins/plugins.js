// Copy a repository URL to the clipboard.
document.querySelectorAll('.repo-row .copy').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var url = btn.parentElement.querySelector('.repo-url').textContent.trim();
    navigator.clipboard.writeText(url).then(function () {
      btn.textContent = 'Copied';
      setTimeout(function () { btn.textContent = 'Copy'; }, 1600);
    });
  });
});

// Show the current version of each plugin from the combined repo.json on this
// site. The version written in the HTML stays if the file cannot be read.
fetch('../repo.json', { cache: 'no-cache' })
  .then(function (r) { return r.ok ? r.json() : []; })
  .then(function (plugins) {
    plugins.forEach(function (p) {
      var el = document.querySelector('.ver[data-plugin="' + p.InternalName + '"]');
      if (el && p.AssemblyVersion) el.textContent = 'v' + p.AssemblyVersion;
    });
  })
  .catch(function () {});
