createbar();
setInterval(withFetch, 2000);

function withFetch(){
    fetch('http://127.0.0.1:5000/prgrss').then(response => response.json()).then(data => document.getElementById("progrss").innerHTML = data.progrss + '%');
    fetch('http://127.0.0.1:5000/prgrss').then(response => response.json()).then(data => document.getElementById("progrssbar").setAttribute('style', 'width: ' + data.progrss + '%'));
}

function createbar () { 
    // create a new div element 
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
