document.getElementById('querybtn').addEventListener('click', submittedQuery);

// var whichQuery = 0;
// queries = [
//     'author/20',
//     'title/20',
//     'random/1',
//     'random/1'
// ]

function submittedQuery() {
    // whichQuery++;
    // if (whichQuery >= 3) {whichQuery = 0;}
    var req;
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
        console.log('created new xmlhttprequest object');
    }
    else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    // var url = 'https://poetrydb.org/' + queries[whichQuery];
    var url = 'https://poetrydb.org/random/1'; 
    req.open('GET', url);
    console.log(url);
    req.onreadystatechange = function () {
        console.log('readystatechange');
        if ((this.readyState == 4) && (this.status == 200)) {
            var resp = JSON.parse(req.responseText);
            // console.log(req.responseText);

            // if (whichQuery == 0) {
            //     console.log('requested author list');
            //     displayReturn(resp.authors);
            // }
            // else if (whichQuery == 1) {
            //     console.log('requested title list');
            //     displayReturn(resp.titles);
            // }
            // else {
            //     console.log('requested random');
            //     displayReturn(resp[0].lines);
            // }
            displayReturn(resp[0].lines);
        }
    };
    req.send();

}

function displayReturn(data) {
    document.getElementById('data').innerHTML = '<ul>';
    for (var i = 0; i < data.length; i++) {
        document.getElementById('data').innerHTML += '<li>' + data[i] + '</li>'; // raw json
    }
    document.getElementById('data').innerHTML += '</ul>';
    console.log('displayed data');
} 
