var getprogressRqst = new XMLHttpRequest();
//getprogress();
setInterval(getprogress, 2000);


function getprogress() {
    getprogressRqst.open("GET", "/prgrss", true);
    //getprogressRqst.onreadystatechange = getProgressData();
    getProgressData();
    getprogressRqst.send();
}

function getProgressData() {
    // if (getprogressRqst.readyState === 4) {
    //     if (getprogressRqst.status === 200) {
            var serverResponse = getprogressRqst.responseText;
            console.log("---------------------------- serverresponse: " + serverResponse);


            //remove tdiv childeren
            var tdiv = document.getElementById("prgrss");

            while (tdiv.hasChildNodes()) {
                tdiv.removeChild(tdiv.lastChild);
            }

            // //update tdiv

            var p = document.createElement("h3");
            p.innerText = serverResponse;

            tdiv.append(p);
    //     }
    // }
}
