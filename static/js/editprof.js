$(document).ready(function() {
	$('#addproj').click(function(){
   		$('.modal').modal('toggle');
	});


	$('#edit_project_form').on('submit', function(event){
		event.preventDefault();
		console.log("form submitted!");
		create_post();
	});
});


function create_post() {
	console.log("create post is working!");
	$('.modal').modal('toggle');

}