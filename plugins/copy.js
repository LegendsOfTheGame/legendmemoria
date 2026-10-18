// Copy a plugin's repository URL to the clipboard.
document.querySelectorAll('.repo-row .copy').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var url = btn.parentElement.querySelector('.repo-url').textContent.trim();
    navigator.clipboard.writeText(url).then(function () {
      btn.textContent = 'Copied';
      setTimeout(function () { btn.textContent = 'Copy'; }, 1600);
    });
  });
});
