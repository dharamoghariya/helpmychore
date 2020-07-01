(function($) {

    var form = $("#signup-form");
    form.steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        labels: {
            previous : 'Prev',
            next : 'Next',
            finish : 'Finish',
            current : ''
        },
        titleTemplate : '<h3 class="title">#title#</h3>',
        onFinished: function (event, currentIndex)
        {
            signup_user();
        }
    });

    $('#signUpAs').parent().append('<ul id="newsignUpAs" class="select-list" name="signUpAs"></ul>');
    $('#signUpAs option').each(function(){
        $('#newsignUpAs').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#signUpAs').remove();
    $('#newsignUpAs').attr('id', 'signUpAs');
    $('#signUpAs li').first().addClass('init');
    $("#signUpAs").on("click", ".init", function() {
        $(this).closest("#signUpAs").children('li:not(.init)').toggle();
    });
    
    var allOptions = $("#signUpAs").children('li:not(.init)');
    $("#signUpAs").on("click", "li:not(.init)", function() {
        allOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#signUpAs").children('.init').html($(this).html());
        allOptions.toggle();
    });


    $('#medicalCondition').parent().append('<ul id="newmedicalCondition" class="select-list" name="medicalCondition"></ul>');
    $('#medicalCondition option').each(function(){
        $('#newmedicalCondition').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    });
    $('#medicalCondition').remove();
    $('#newmedicalCondition').attr('id', 'medicalCondition');
    $('#medicalCondition li').first().addClass('init');
    $("#medicalCondition").on("click", ".init", function() {
        $(this).closest("#medicalCondition").children('li:not(.init)').toggle();
    });

    var allOptions = $("#medicalCondition").children('li:not(.init)');
    $("#medicalCondition").on("click", "li:not(.init)", function() {
        allOptions.removeClass('selected');
        $(this).addClass('selected');
        $("#medicalCondition").children('.init').html($(this).html());
        allOptions.toggle();
    });
    
})(jQuery);

function signup_user(){

json_data = {
"email":$("#email").val(),
"name":$("#name").val()
}
$.ajax({
    url:"/signup_user",
    type:"POST",
    data: JSON.stringify(json_data),
    dataType: "json",
    contentType: "application/json"
    }).done(function (data){
        if(data=="success"){
            alert("registered successfully");
        }
    })
}
