
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    var cve_id = document.getElementById('cve_id').value;
    var action_url = '/cve/' + cve_id;

    this.setAttribute('action', action_url);

    this.submit();
});
