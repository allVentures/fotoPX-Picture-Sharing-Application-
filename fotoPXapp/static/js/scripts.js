$(function () {
    var $registrationForm = $('#formRegister');
    var $voivodeshipSelect = $('#voivodeship').find('select');


    $registrationForm.on('submit', function (e) {
        e.preventDefault();

    });

    $voivodeshipSelect.on('change', function (e) {
        var id = $(this).val();
        getCounties(id);
    });

    function getCounties(id) {
        console.log(id);
        $.ajax({
            url: "/rejestracja",
            data: {"voivodeship_id": id},
            type: "GET",
            dataType: "json"
        }).done(function (json) {
            generateCountiesList(json);
        }).fail(function (xhr, status, err) {
        }).always(function (xhr, status) {
        });
    }

    function generateCountiesList(countiesList) {
        var $newEl = `
            <div class="form-group" id="voivodeship">
            <label>Powiat:</label>
            <select name="regions" class="form-control">`;
        for (const el in countiesList) {
            $newEl += `<option value="${el}">${countiesList[el]}</option>\n`;
        }
        $newEl += `</select></div>`;
        $('#voivodeship').after($newEl);
    }
});







