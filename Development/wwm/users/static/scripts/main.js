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
				$('body').append(overlay);
				$(overlay).addClass("flex");
				$(overlay).css("position", "absolute");
				$(overlay).css("height", "100vh");
				$(overlay).css("width", "100vw");
				$(overlay).css("top", "0");
				$(overlay).css("left", "0");
				$(overlay).css("background-color", "rgba(0,0,0,0.5)");
				iframe.src = "/static/forms/" + type + ".html";
				$(overlay).append(iframe);
			},
			close: function()
			{
				var overlay = this.overlay;
				$(overlay).remove();
			}
		};
	return tmpModal;
}
