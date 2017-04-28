$(document).ready(function() {
	$('#addproj').click(function(){
   		$('.modal').modal('toggle');
	});


	$('#edit_project_form').on('submit', function(event){
		event.preventDefault();
		//data does not include the image. need to turn into array where one part is data dn other part is the iamge
		
		$.post("edit_project/");
		console.log("form submitted!");
		close_modal();
	});
});


function close_modal() {
	$('.modal').modal('toggle');
}

