function getAppointment(appointment_id, url){
    $.ajax({
        type: "POST",
        url: url,   
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            id:appointment_id
        },
        success: function(result){
            alert("se reservo pero nada mas") 
            init_Materialize()
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    });  
}
function loadAppointments(doctor_id, url){
    $.ajax({
        type: "GET",
        url: url,   
        data: {
            doctor_id:doctor_id
        },
        success: function(result){
            $("#block-" + doctor_id).html(result)        
            $("#block-" + doctor_id).css("display", "block")
            $("#btn-" + doctor_id).text("ACTUALIZAR")
            init_Materialize()
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    });  
}
function loadWorkDayHtml(){
    $.ajax({
        type: "GET",
        url: "{% url 'loadWorkDayForm' %}",   
        success: function(result){
            $("#card").html(result)        
            $("#card").css("display", "block")
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    });  
}
function removeWorkDay(workday_id, url){
    $.ajax({
        type: "POST",
        url: url,
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            workday_id: workday_id
        },
        success: function(result){
            window.location.href = "{% url 'profile' %}"; 
        },
        error: function (request, status, error){
                alert(request.responseText)
        }
    })
}

function deleteAppointment(appointment_id, url){
    $.ajax({
        type: "POST",
        url: url,   
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            appointment_id:appointment_id
        },
        success: function(result){
            window.location.href = "{% url 'profile' %}"; 
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    })
}