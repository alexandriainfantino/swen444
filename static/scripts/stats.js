//Build the bar chart
var ctx = document.getElementById("barChart");
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Low","Medium", "High"] ,
        datasets: [{
            label: "Donation Distribution",
            //This is hardcoded for now, we will replace this with API call
            data: [50,70,24],
            backgroundColor: ['#E0E0E0','#C8E6C9','#D1C4E9'],
            borderColor: ['#E0E0E0','#4CAF50','#673AB7'],
            borderWidth: 1
        }]
    },
    options: {
        response: true,
        maintainAspectRatio: false,
        scale: {
            yAxes: [{
                ticks: {
                    beginAtZero: true    
                }
            }]    
        }
    }
});



//Build the line graph
var ctx1 = document.getElementById("lineChart");
var myChart = new Chart(ctx1, {
    type: 'line',
    data: {
        labels: ["Feb","March","April","May","June","July","August"],
        datasets: [
            {
                label: "Donations per month by number",
                fillColor: "#4CAF50",
                strokeColor: "#4CAF50",
                data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
                label: "Donations per month by amount",
                fillColor: "#673AB7",
                stokeColor: "673AB7",
                data: [10, 65, 150, 100, 40, 60, 24]
            },
        ],
   },
    options: {
        response: true,
        maintainAspectRatio: false
   }
});


