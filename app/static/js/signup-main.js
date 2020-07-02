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
    
    var allOptionsCat = $("#signUpAs").children('li:not(.init)');
    $("#signUpAs").on("click", "li:not(.init)", function() {
        allOptionsCat.removeClass('selected');
        $(this).addClass('selected');
        $("#signUpAs").children('.init').html($(this).html());
        allOptionsCat.toggle();
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

    var allOptionsCond = $("#medicalCondition").children('li:not(.init)');
    $("#medicalCondition").on("click", "li:not(.init)", function() {
        allOptionsCond.removeClass('selected');
        $(this).addClass('selected');
        $("#medicalCondition").children('.init').html($(this).html());
        allOptionsCond.toggle();
    });
    
})(jQuery);

function signup_user(){
    category = $("#signUpAs").children('.init').text();
    medicalCondition = $("#medicalCondition").children('.init').text();

    if(category == "" || medicalCondition == ""){
        alert("Please fill up all the fields to continue");
        return false;
    }
    if(category == "Volunteer" && medicalCondition == "Yes"){
        alert("Sorry we cannot let you volunteer with medical conditions");
        return false;
    }
    json_data = {
        "name":$("#name").val(),
        "email":$("#email").val(),
        "age":$("#age").val(),
        "phone":$("#phone").val(),
        "unitNo":$("#unitNo").val(),
        "streetNo":$("#streetNo").val(),
        "streetName":$("#streetName").val(),
        "city":$("#city").val(),
        "postalCode":$("#postalCode").val(),
        "province":$("#province").val(),
        "username":$("#username").val(),
        "password":$("#password").val(),
        "category":category,
        "medicalCondition":medicalCondition
    }
    $.ajax({
            url:"/signup_user",
            type:"POST",
            data: JSON.stringify(json_data),
            dataType: "json",
            contentType: "application/json"
        }).done(function (data){
            window.location.replace("login");
        })
}


$('#login_user').click(function(e){

    json_data = {

        "username":$("#username").val(),
        "password":$("#password").val()
    }
    $.ajax({
            url:"/login_user",
            type:"POST",
            data: JSON.stringify(json_data),
            dataType: "json",
            contentType: "application/json"
        }).done(function (data){
            if(data == 200){
            window.location.replace("errands");
            }
        })
});