//somebody who in charge of fetching html form data and get it to javascript
// u can hit enter and see the input value on the console if u put some data in any of the input field
//or u can do specific id jquey select, i only did for the first one as example. U may need to figure out way to do the rest.

//$("input[type='text'").keypress(function(e){
//	if (e.which === 13){
//		console.log($(this).val());
//	}
//});

var coll = document.getElementsByClassName("collapsibleBtn");
var collcon = document.getElementsByClassName("collapsibleContent");
var nextBtn = document.getElementById("nextBtn");
var i;
var activeCon = 0;

function openContent(i) {
    coll[activeCon].classList.toggle("active");
    collcon[activeCon].style.maxHeight = null;

    var content = collcon[i];
    coll[i].classList.toggle("active");
    content.style.maxHeight = content.scrollHeight + "px";
    activeCon = i
}


for (i = 0; i < coll.length; i++) {
    let x = i;
    coll[x].addEventListener("click", function() {
        openContent(x)
    });
}

var n = 1;
nextBtn.addEventListener("click", function() {
    if (n > coll.length) {
        nextBtn.setAttribute('type', 'submit');
    }
    if (n < coll.length ) {
        coll[n].style.display = "block";
        openContent(n)
        n += 1;
    } 
    if (n == coll.length) {
        nextBtn.innerHTML = "Submit";
        nextBtn.style.backgroundColor = "#fcae1e";
        n += 1;
    }
});


var content = collcon[0];
coll[0].style.display = "block";
coll[0].classList.toggle("active");
content.style.maxHeight = content.scrollHeight + "px";
