const searchInput = document.getElementById('search');
const table = document.getElementById('table');
const tableRows = table.getElementsByTagName('tr');

searchInput.addEventListener('keyup', function() {
  const searchTerm = searchInput.value.toLowerCase();
  for (let i = 1; i < tableRows.length; i++) {
    const rowText = tableRows[i].innerText.toLowerCase();
    if (rowText.includes(searchTerm)) {
      tableRows[i].style.display = '';
    } else {
      tableRows[i].style.display = 'none';
    }
  }
});
