$(document).ready(function(){

  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  $('table').on('click', 'button[type="submit"]', function(e){
    var user_stock_id = $(this).data();
    //$(this).closest('tr').remove()
    $.ajax({
      type:"POST",
      url: "/home/delete/",
      data: user_stock_id,
      success: function(result) {
        console.log("stock tracker deleted from db");
      },
      error: function(result) {
        console.log("returned error. stupid.");
      }
    })
  })


})
