(function () {
  var form = document.getElementById('undtagelser');
  if (!form) return;
  var rows = Array.prototype.slice.call(form.querySelectorAll('[data-linje]'));
  var msg = document.getElementById('msg');

  function felt(row, k) { return row.querySelector('[data-felt="' + k + '"]'); }

  function opdater() {
    var klar = 0;
    rows.forEach(function (row) {
      var t = felt(row, 't').value, z = felt(row, 'z'), i = felt(row, 'i'), d = felt(row, 'd'), st = felt(row, 'st');
      var selv = t === 'selv';
      z.disabled = !selv;
      i.disabled = !selv;
      if (!selv) { z.value = ''; i.checked = false; }
      d.disabled = !(selv && i.checked);
      if (d.disabled) d.value = '';
      var dage = Number(d.value), tekst, klasse;
      if (row.dataset.satsMangler) { tekst = 'Mangler sats'; klasse = 'bad'; }
      else if (!t) { tekst = 'Mangler transport'; klasse = 'warn'; }
      else if (selv && !z.value) { tekst = 'Mangler zone'; klasse = 'bad'; }
      else if (selv && i.checked && !(Number.isInteger(dage) && dage >= 1 && dage <= 31)) { tekst = 'Mangler dage'; klasse = 'bad'; }
      else { tekst = 'Klar'; klasse = 'ok'; klar++; }
      st.textContent = tekst;
      st.className = 'badge ' + klasse;
      st.title = '';
    });
    document.getElementById('cnt').textContent = klar + ' af ' + rows.length + ' klar';
    return rows.length - klar;
  }

  form.addEventListener('input', function () { msg.textContent = ''; msg.className = 'msg'; opdater(); });
  document.getElementById('beregn').addEventListener('click', function (e) {
    var mangler = opdater();
    if (mangler > 0) {
      e.preventDefault();
      msg.className = 'msg bad';
      msg.textContent = mangler + (mangler === 1 ? ' borger mangler' : ' borgere mangler') + ' oplysninger, før du kan beregne';
    }
  });
  opdater();
})();
