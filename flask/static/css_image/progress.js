var getprogressRqst = new XMLHttpRequest();
//getprogress();
setInterval(getprogress, 2000);


function getprogress() {
    getprogressRqst.open("GET", "/prgrss", true);
    var serverResponse = getprogressRqst.responseText;
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
