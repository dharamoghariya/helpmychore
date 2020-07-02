/* custom JS for Dashboard*/

function request_submit(){
    groceryStores = $('#input-grocery-store').val()
    groceryList = $('#input-grocery-list').val()
    notes = $('#input-grocery-notes').val()

    requestInfo = "Preferred stores: " + groceryStores +"<br>Grocery List: " + groceryList


    json_data = {

        "request_information":requestInfo,
        "request_note":notes,
        "request_type": "grocery_delivery"
    }
    $.ajax({
            url:"/submit_request",
            type:"POST",
            data: JSON.stringify(json_data),
            dataType: "json",
            contentType: "application/json"
        }).done(function (data){
            if(data == 200){
            $('#request-success-alert').removeClass('hide');
            }else{
            $('#request-error-alert').removeClass('hide');
            }
        })
}


function fetch_requests(){
    request_results = ""
    $.ajax({
            url:"/get_requests",
            type:"POST",
            dataType: "json",
            contentType: "application/json"
        }).done(function (data, status_code){
            if(status_code == "success"){
                $.each(data, function(key, jData){
                request_results += "<tr>";
                request_results += "<td>"+jData.request_date+"</td>";
                request_results += '<th scope="row"><div class="media align-items-center"><div class="media-body"><span class="name mb-0 text-sm">'+jData.request_type+'</span></div></div></th>';
                request_results += '<td>'+jData.street_name+'</td>';
                request_results += '<td>'+jData.city+'</td>';
                request_results += '<td> <a href="#">Take this Task</a></td>';
                request_results += "</tr>";
                });
                $('#requests_list').html(request_results)

            }

        })
}