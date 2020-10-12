// the location of this file is required for flask to find the js script

// call for creation progressbar
createbar();
// check (fetch) progress every 2 seconds
setInterval(withFetch, 2000);

function withFetch(){
    // this line is for the async request for progress number we see on the succes page
    fetch('http://127.0.0.1:5000/prgrss').then(response => response.json()).then(data => document.getElementById("progrss").innerHTML = data.progrss + '%');
    // this line changes the style of the progress bar with a async request for the number of the progress
    fetch('http://127.0.0.1:5000/prgrss').then(response => response.json()).then(data => document.getElementById("progrssbar").setAttribute('style', 'width: ' + data.progrss + '%'));
}

// function to create the progressbar on the success page
function createbar () { 
    const bar = document.createElement("div"); 
    
    bar.setAttribute('class', 'progress-bar');
    bar.setAttribute('id', 'progrssbar')
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('style', 'width: 0%');
    bar.setAttribute('aria-valuenow', 'O');
    bar.setAttribute('aria-valuemin', 'O');
    bar.setAttribute('aria-valuemax', '10O');

    document.getElementById("progrsss").appendChild(bar); 
}
