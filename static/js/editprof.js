$(document).ready(function() {
	$('#addproj').click(function(){
   		$('.modal').modal('toggle');
	});


	$('#edit_project_form').on('submit', function(event){
		event.preventDefault();
		let data = new FormData($(this)[0]);
		let options = {
			url: $(this).attr('action'),
			data: data,
			contentType: false,
			processData: false,
			type: 'POST',
			success: function(response) {
				$('#edit_project_form')[0].reset();
				$('.modal').modal('toggle');
				render_project(response);
            }
		}
		$.ajax(options);
		console.log("form submitted!");
		//create_post();
	});
});

function render_project(project) {
	// render it
	console.log(project);
}
// function create_post() {
// 	console.log("create post is working!");
// 	$('.modal').modal('toggle');
//
// }