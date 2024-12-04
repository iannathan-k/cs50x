function revealAnswer(id) {

    const elem = document.getElementById("answer" + id);
    if (elem) {
        elem.className = "";
    }

    const buttonElem = document.getElementById("button" + id);
    if (buttonElem)
        buttonElem.className = "d-none";
    const yesElem = document.getElementById("yes" + id);
    if (yesElem)
        yesElem.classList.remove('disabled');
    const noElem = document.getElementById("no" + id);
    if (noElem)
        noElem.classList.remove('disabled');
}

function ama(questionid) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/ama");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("questionid=" + questionid);
}

function grading(batchid, id, correct) {

    const yesElem = document.getElementById("yes" + id);
    if (yesElem)
        yesElem.className = "d-none";
    const noElem = document.getElementById("no" + id);
    if (noElem)
        noElem.className = "d-none";

    const resultElem = document.getElementById("result" + id);
    var result = correct ? "correct" : "incorrect";
    var color = correct ? "green" : "red";
    if (resultElem) {
        resultElem.innerHTML = result;
        resultElem.className = color;
    }

    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/grading");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("batchid=" + batchid + "&correct=" + correct);
}
