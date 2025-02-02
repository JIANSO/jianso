function show_contents(d){
    $.ajax({

      type: 'post'
      ,data : {type : d}
      ,url: '/bp_church/contents/' + d 
      ,success: function(response) {
        $('#inner_list').html(response); 
      }
      ,error: function(error) {
        console.log(error);
      }
    });
  }