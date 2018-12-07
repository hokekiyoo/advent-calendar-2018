var ctx = document.getElementById('myChart').getContext('2d');
var ws;
ws = new WebSocket("ws://127.0.0.1:9999/websocket");

  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
				labels:["1","2","3","4","5","6","7","8","9","10","11","12"],
      datasets: [{
        label: "temp",
		  data :[0,0,0],
        backgroundColor: "rgba(153,255,51,0.4)"
      },],
			options:{
				scale:{
					yAxes:{
						ticks:{
							min : 20,
							max : 40
							}
						}
					}
				}
    }
  });
console.log(myChart.config.data.datasets[0].data);
ws.onmessage = function(ev) {
  var data = JSON.parse(ev.data);
  var keys = Object.keys(data); 
  console.log(keys);
  console.log(data);
  var newdata = data["temp"]; 
  myChart.config.data.datasets[0].data = newdata;
  myChart.update();
}
function sendAction() {
  ws.send("message");
  console.log("hoge");
  
}

$(document).ready(function() {
  $("#send").click(function(){
      sendAction();
  });
});