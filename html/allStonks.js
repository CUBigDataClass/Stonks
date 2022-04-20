// js file to listen to post requests from allstonks.html
function handleSubmit(){
    const new_url = document.getElementById('test').value;
    localStorage.setItem("URL", new_url);

    return;
}