//get name from all stonks html input and remove
var r = location.search.substring(1).split("&");
//parsing values
var parse = r.toString();
const key = parse.substring(0, parse.indexOf("="));
//console.log(key);

