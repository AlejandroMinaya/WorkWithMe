var Modal = function(type)
{
	var tmpModal = 
		{
			type: type,
			overlay: document.createElement("div"),
			iframe: document.createElement("iframe"),

			load: function()
			{
				var overlay = this.overlay;
				var iframe = this.iframe;
				var modal = this;
				$('body').append(overlay);
				$(overlay).addClass("flex");
				$(overlay).css("position", "absolute");
				$(overlay).css("height", "100vh");
				$(overlay).css("width", "100vw");
				$(overlay).css("top", "0");
				$(overlay).css("left", "0");
				$(overlay).css("background-color", "rgba(0,0,0,0.5)");
				iframe.src = "/static/forms/" + type + ".html";
				$(iframe).css("height", "80vh");
				$(iframe).css("width", "80vw");
				$(iframe).css("background-color", "#fff");
				$(iframe).css("border-radius", "50px");
				$(iframe).css("border", "none");
				$(iframe).css("box-shadow", "0 0 10px 0 rgba(0,0,0,.3)");
				$(overlay).append(iframe);
				$(overlay).click(function(){modal.close()});
			},
			close: function()
			{
				var overlay = this.overlay;
				$(overlay).remove();
				location.href = "";
			}
		};
	tmpModal.load();
	return tmpModal;
}

//TASKS
//-- VERIFY
var markTaskForVerification = function(_taskID)
{
	$.post("/tasks/markTaskForVerification",{
		taskID: _taskID
	},function(data, status){
		console.log("Task marked for verification");
		location.href="";
	});
}
