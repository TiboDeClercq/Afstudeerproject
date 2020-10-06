var getprogressRqst = new XMLHttpRequest();
//getprogress();
//setInterval(getprogress, 2000);
setInterval(withFetch, 2000);


function withFetch(){
    fetch('http://127.0.0.1:5000/prgrss').then(response => response.json()).then(data => document.getElementById("progrss").innerHTML = data.progrss);
}


function getprogress() {
    getprogressRqst.open("GET", "/prgrss", true);
    var serverResponse = getprogressRqst.responseText;
    //var serverResponse = Response.progrss;
    //var serverResponse = JSON.parse(getprogressRqst.responseText);
    console.log("---------------------------- serverresponse:-" + serverResponse + "_");
    document.getElementById("progrss").innerHTML = serverResponse;
    //getprogressRqst.onreadystatechange = getProgressData();
    //getProgressData();
    getprogressRqst.send();
}

// function getProgressData() {
//     if (getprogressRqst.readyState === 4) {
//         if (getprogressRqst.status === 200) {
//             var serverResponse = getprogressRqst.responseText;
//             console.log("---------------------------- serverresponse:-" + serverResponse + "_");
//             document.getElementById("progrss").innerHTML = serverResponse;
//         }
//     }
// }
