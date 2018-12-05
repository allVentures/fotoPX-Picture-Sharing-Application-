$(function () {
// --------------------JS START-------------------------
// ------------REGIONS---------------
    var $registrationForm = $('#formRegister');
    var $voivodeshipSelect = $('#voivodeship').find('select');


    // $registrationForm.on('submit', function (e) {
    //     e.preventDefault();
    //
    // });

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
            <div class="form-group" id="regions">
            <label>Powiat:</label>
            <select name="regions" class="form-control">
            <option value="0">... wybierz Powiat! ...</option>`;

        for (const el in countiesList) {
            $newEl += `<option value="${el}">${countiesList[el]}</option>\n`;
        }
        $newEl += `</select></div>`;
        $('#voivodeship').after($newEl);

        var $regionsSelect = $('#regions').find('select');
        $regionsSelect.on('change', function (e) {
            var county_id = $(this).val();
            console.log(county_id)
            voivodeship_id = $voivodeshipSelect.val();
            console.log(voivodeship_id);
            getCities(county_id, voivodeship_id);
        });
        $voivodeshipSelect.attr("disabled","True");
    }

    function getCities(county_id, voivodeship_id) {
        $.ajax({
            url: "/rejestracja",
            data: {"voivodeship_id": voivodeship_id, "county_id": county_id},
            type: "GET",
            dataType: "json"
        }).done(function (json) {
            generateCitiesList(json);
        }).fail(function (xhr, status, err) {
        }).always(function (xhr, status) {
        });
    }

    function generateCitiesList(json) {

        var $newEl = `
            <div class="form-group" id="cities">
            <label>Gmina:</label>
            <select name="regions" class="form-control">
            <option value="0">... wybierz Gminę! ...</option>`;
        for (const el in json) {
            $newEl += `<option value="${el}">${json[el]}</option>\n`;
        }
        $newEl += `</select></div>`;
        $('#regions').after($newEl);
        $('#regions').find('select').attr("disabled","True");

    }

// ------------PICTURES GRID---------------
    var $pictures = $(".pictureThumbnail");
    $pictures.each(function (i) {

        var w = parseInt($(this).attr("data-width"));
        var h = parseInt($(this).attr("data-height"));

        var flexBasis = (w * 140) / h;
        var flexGrow = (w * 100) / h;
        var paddingBottom = (h / w) * 100;


        var src = $(this).attr('src');
        // console.log(src);

        $(this).css({
            'opacity': 0
        });

        $(this).parent('a').wrap('<figure>')
        // $(this).before('<i>');

        var figure = $(this).parent().parent();
        figure.css({
            'flex-grow': flexGrow,
            'flex-basis': flexBasis + 'px',
            'background-image': 'url(' + src + ')'
        });

        // figure.find('i').css({
        //     'padding-bottom': paddingBottom + '%'
        // });


        var img = new Image();
        img.onload = function () {
            figure.addClass('loaded');
        }
        img.src = src;
    });

// all picture display flex end

// --------------------JS END -------------------------
});
