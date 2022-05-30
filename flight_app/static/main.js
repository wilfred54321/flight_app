$(':checkbox.all').change(function () {
    $(':checkbox.item').prop('checked', this.checked);
});