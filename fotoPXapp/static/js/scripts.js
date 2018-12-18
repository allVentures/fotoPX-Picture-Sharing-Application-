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
            <select name="county_id" class="form-control">
            <option value="0">... wybierz Powiat! ...</option>`;

        for (const el in countiesList) {
            $newEl += `<option value="${el}">${countiesList[el]}</option>\n`;
        }
        $newEl += `</select></div>`;
        $('#voivodeship').after($newEl);

        var $regionsSelect = $('#regions').find('select');
        $regionsSelect.on('change', function (e) {
            var county_id = $(this).val();
            voivodeship_id = $voivodeshipSelect.val();
            getCities(county_id, voivodeship_id);
        });
        $voivodeshipSelect.on('change', function (e) {
            $('#regions').remove();
            $('#cities').remove();
        });
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
            <select name="municipality_id" class="form-control">
            <option value="0">... wybierz Gminę! ...</option>`;
        for (const el in json) {
            $newEl += `<option value="${el}">${json[el]}</option>\n`;
        }
        $newEl += `</select></div>`;
        $('#regions').after($newEl);
        $('#regions').find('select').on('change', function (e) {
            $('#cities').remove();
        });

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

//--------------- Picture comments input size ---------------
    var $commentInput = $('.form-control.commentInput');
    $commentInput.on('input', function (e) {
        var scroll_height = $(this).get(0).scrollHeight;
        if (scroll_height > 60) {
            $(this).css('height', scroll_height + 'px');
        }
    });
    $commentInput.on('keydown', function (e) {
        if ((e.keyCode == 46) || (e.keyCode == 8)) {
            var scroll_height = $(this).get(0).scrollHeight;
            $(this).css('height', scroll_height - 200 + 'px');
        }
    });

// ---------------Picture comments  - Add Comment ---------------
    var $buttonComment = $('.buttonAddComment');
    $buttonComment.on('click', function (e) {
        var url = $(location).attr('href');
        var $pictureComment = $('#id_comment').val();
        $.ajax({
            url: url,
            data: {"picture_comment": $pictureComment},
            type: "GET",
            dataType: "json"
        }).done(function (json) {
            add_new_picture_comment(json);
        }).fail(function (xhr, status, err) {
        }).always(function (xhr, status) {
        });
    })

    function add_new_picture_comment(comment) {
        var $new_comment = `
     <li class="media comments">
        <a href="/${comment["commenter_slug"]}">
            <img class="mr-3 commentAvatar" src="/media/${comment["commenter_avatar"]}" alt="">
        </a>
        <div class="pictureComment">
            <a href="/${comment["commenter_slug"]}">${comment["commenter_name"]}</a>
            <div class="media-body">
            ${comment["comment"]}
            </div>
        </div>
    </li>`;
        $('#pictureCommentLi').after($new_comment);
        $('#pictureCommentLi textarea').val('');
    }

    //----------Picture rating---------------

    $('.PictureRating input').change(function () {
        var url = $(location).attr('href');
        var $radio = $(this);
        var $rating = $radio.val();
        $('.PictureRating .selected').removeClass('selected');
        $radio.closest('label').addClass('selected');
         $.ajax({
            url: url,
            data: {"rating": $rating},
            type: "GET",
            dataType: "json"
        }).done(function (json) {
            $('#pic_av_rating').text(json.pic_average_rating);
            $("#your_rating").text("Twoja ocena:");
        }).fail(function (xhr, status, err) {
        }).always(function (xhr, status) {
        });
    });


// --------------------JS END -------------------------
});

