// Name: Bob Borsboom
// Student number: 10802975
// Data Processing WK2
//
// Create a line graph of the temperature at De Bilt weather station
// during the year 2014

window.onload = function() {
 
    function loading(loaded_data){
    	var date = [];
		var temperture = [];

		x_text = ["2014", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		
		// load the dates into a the date array
		for (var i = 0; i < 365; i++){

			// select al the dates
			var maxtemp = loaded_data.split("\n")[i];
			var test = maxtemp.split(",")[0]

			// reformat date to 2014-01-01
			var year = test.slice(0,4) + "-";
			var month = test.slice(4,6) + "-";
			var day = test.slice(6,8);

			var make_date = new Date(year + month + day)

			// reformate days to milliseconds
			make_seconds = make_date.getTime()
			
			// number of milliseconten per day is 86 400 000
			// 16 070 is the number of days since is was 1 jan 1970
			make_days = (make_seconds / 86400000) - 16070
			
			date.push([make_days]);
		}	

		// load the tempertures into a the temperture array
		for (var i = 0; i <365; i++){

			// select all the tempertures
			var maxtemp = loaded_data.split("\n")[i];
			var test = maxtemp.split(",")[1].trim()

			temperture.push([test]);
		}
		
		// set up the canvas
		var canvas = document.getElementById("myCanvas");
		var ctx = canvas.getContext("2d")
		
		// range of tempertures, range on canvas y axis
		var canvas_point_y = createTransform([0, 350], [170, 30])
		// range of days, range on canvas x axis
		var canvas_point_x = createTransform([1, 365], [35, 330])

		ctx.beginPath();

		// draw all the date and temperture points and draw lines between
		for (var i = 0; i < date.length; i++){

			// sign the first pixel 
			ctx.moveTo(canvas_point_x(date[i]), canvas_point_y(temperture[i]));

			// sign the seconds pixel
			ctx.lineTo(canvas_point_x(date[i+1]), canvas_point_y(temperture[i+1]));

			// sign a line from the first, to the second pixel
			ctx.stroke();
		}

		// canvas title text
		ctx.fillText("Maximum temperture in De Bilt (NL)", 200, 20);

		// line on the x axis
		ctx.beginPath();
		ctx.moveTo(35, 170);
		ctx.lineTo(330, 170);
		ctx.closePath();
		ctx.stroke();

		// sublines op de x axis
		ctx.beginPath();
		// (330 - 35) / 11 = 26.818
		// 26.818 * 12 = 321
		for (var i = 0; i < 321; i += 26.818){
			ctx.moveTo((35 + i), 170);
			ctx.lineTo((35 + i), 175);
			ctx.closePath();
			ctx.stroke();		
		}

		// line on the y axis
		ctx.beginPath();
		ctx.moveTo(30, 25);
		ctx.lineTo(30, 170);
		ctx.closePath();
		ctx.stroke();

		// subline on the y axis
		ctx.beginPath();
		// 145 / 7 = 20.714
		for (var k = 0; k < 145; k += 20.714 ){
			ctx.moveTo(30, 25 + k);
			ctx.lineTo(20, 25 + k);
			ctx.closePath();
			ctx.stroke();		
		}

		// text along the y axis
		for (var i = 0; i < 8; i++){
			y = 20.714 * i
			ctx.fillText(350 - (50 * i), 2, (y + 28));
		}

		//text along the x axis x as
		ctx.translate(canvas.width - 180, 25 );
		ctx.rotate(45 * Math.PI / 180);
		for (var i = 0; i < 12; i++){
			j = 19* i
			ctx.fillText(x_text[i], j , 200 - j + 25);
		}
    }
	
	// set function in variable
	var server = new XMLHttpRequest();

	// when variable retreives data, call the function
	server.onreadystatechange = function() {

	// check if everything is received (4) and if it goes to the right page(200) 
    if (this.readyState == 4 && this.status == 200) {

       loading(server.responseText)
    }
}
	// server opens the data file
	server.open("GET", "KNMI.txt", false);
	server.send();

	function createTransform(domain, range){
		// domain is a two-element array of the data bounds [domain_min, domain_max]
		// range is a two-element array of the screen bounds [range_min, range_max]
		// this gives you two equations to solve:
		// range_min = alpha * domain_min + beta
		// range_max = alpha * domain_max + beta
	 		// a solution would be:

	    var domain_min = domain[0]
	    var domain_max = domain[1]
	    var range_min = range[0]
	    var range_max = range[1]

	    // formulas to calculate the alpha and the beta
	   	var alpha = (range_max - range_min) / (domain_max - domain_min)
	    var beta = range_max - alpha * domain_max

	    // returns the function for the linear transformation (y= a * x + b)
	    return function(x){
	      return alpha * x + beta;
	    }
	}
}





