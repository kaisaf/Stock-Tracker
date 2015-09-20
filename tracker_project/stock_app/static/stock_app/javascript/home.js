$(document).ready(function(){

  $('table').on('click', 'button[type="submit"]', function(e){
    var user_stock_id = $(this).data();
    $(this).closest('tr').remove()
    $.ajax({
      type:"POST",
      url: "delete/",
      data: user_stock_id,
      success: function(result) {
        console.log("UserStock instance deleted from db");
      },
      error: function(result) {
        console.log("Something went wrong");
      }
    })
  })
})
