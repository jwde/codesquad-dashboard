var projectTitles = [];


$(document).ready(function() {
	var projectList = document.getElementById('projectList'); 
	var projectArray = JSON.parse(projects);
	console.log(projectArray);



	for (project in projectArray)
	{
		console.log(projectArray[project]);
		var image = "<image class='pectImages' src ='" + projectArray[project]['image'] +"' alt='Project Title: " + projectArray[project]['title'] + "'/>"
		image.click = openProjectInfo(projectArray[project]['title']);
		$("#projectList").append("<li class='projectList' id='project_" + project + "'>" + image + "</li>");
	}
	//projectList.innerHTML = projectArray[0]['title'];
	var projectTable = document.createElement("TABLE");

	// Use project array to fill in the information
	$('#projectList').on('click', 'li', function() {
		$('#project_title').innerHTML= $(this).attr('id');
		$('.modal').modal('toggle');
		console.log("I am project_"+$(this).attr('id'));
	});
});




function openProjectInfo(projectTitle)
{
	console.log(projectTitle);
}