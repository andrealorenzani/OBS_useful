var data = {};
var result = {};
var isUpAndRunning = false;

$( document ).ready(function() {

	$.ajaxSetup({
	  contentType: "application/json"
	});

	sendData({});

	setInterval(function() { checkStatus(); }, 10000);

	$("#forms > div").hide();

	$(".state").prepend('<img src="banner_1.jpg" style="width: 766px" />');

	$('#forms').ready(function() {
		showPanel( $( '#intro' )); 
	} );
});

function waitResult(panel) {
	showPanel(panel);
	sendData(data, function (res) { 
		setTimeout(function(){
		result = res;
		console.log(result);
		hideAndShow(panel, $( '#result' ) );
	}, 1000); }, 
		function () {
			hideAndShow(panel, $( '#email' ));
		});
}

function display(panel) {
	if (result == null || typeof result != 'object') {
		result = {};
	}
	var value = Object.keys(result)[0];
	panel.find('.state_content').empty();
	for(item in result[value]) {
		panel.find('.state_content').append('<p>'+result[value][item]+'</p>');
	}
	panel.find('.state_content').append('<p><img class="accept" data-next="result" src="accept.png" style="height: 55px; padding: 10px;"/></p>')
	delete result[value];
	if(Object.keys(result).length == 0){
		panel.find('.accept').attr('data-next', 'name_surname')
	}
	showPanel(panel);
}

function defaultFail(){
	$( ".server_status_text" ).css('color', 'red');
	$( ".server_status_text" ).text('down');
	$( ".server_status_img").attr('src', 'server_down.png');
	isUpAndRunning = false;
}

function defaultSuccess(){
	$( ".server_status_text" ).css('color', 'lightgreen');
	$( ".server_status_text" ).text('up');
	$( ".server_status_img").attr('src', 'server_up.png');
	isUpAndRunning = true;
}

function checkStatus(){
	$.get( "compute.php", {}, function (returndata, status, xhr) {
	  	if(["error", "timeout", "parsererror"].includes(status)) {
	  		defaultFail();
	  	}
	  	else {
	  		defaultSuccess();
	  	}
	  }).fail(function(){
	  	defaultFail();
	  });
}

function sendData(sendData = data, func = function() {}, fail = function() {}){
	$.post( "compute.php", JSON.stringify( sendData ), function (returndata, status, xhr) {
	  	if(["error", "timeout", "parsererror"].includes(status)) {
	  		fail();
	  		defaultFail();
	  	}
	  	else {
	  		func(returndata);
	  		defaultSuccess();
	  	}
	  }).fail(function(){
	  	fail();
	  	defaultFail();
	  });
}

function clear(panel) {
	data = {};
	showPanel(panel);
}

function showPanel(panel) {
	var panelWidth = panel.width();
	var totalWidth = $( document ).width();
	var panelheight = panel.height();
	var totalHeight = $( document ).height();
	totalHeight = totalHeight>panelheight? totalHeight : panelheight;
	totalWidth = totalWidth>panelWidth? totalWidth : panelWidth;
	var positionh = (((totalHeight - panelheight)*50)/totalHeight)+'%';
	var positionw = (((totalWidth - panelWidth)*50)/totalWidth)+'%';
	panel.parent().css('height', totalHeight+'px');
	panel.css({'left':'-'+panelWidth+'px', 'top':positionh, 'opacity': 0});
	panel.show();
	panel.animate({left: positionw, 'opacity': 1},750);
	panel.find('.accept').click(function() {
		if ($( this ).attr('data-value')) {
			data[panel.attr('id')] = $( this ).attr('data-value');
		}
		panel.find('input').each(function () {
			data[$( this ).attr('name')] = $( this ).val();
		});
	  	hideAndShow(panel, $( '#'+$( this ).attr('data-next') ) );
	})
}

function hideAndShow(hideP, showP) {
	var totalPosition = hideP.parent().width();
	hideP.stop().animate({left: totalPosition+'px', 'opacity': 0},750, function() {
		if (showP.attr('data-function')) {
			var funName = showP.attr('data-function');
			window[funName](showP);
		}
		else {
			showPanel(showP);
		}
	});
}