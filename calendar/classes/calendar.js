
function dropdownItem(id){
    document.getElementById(id).classList.toggle("show");
}

function selectDropdownItem(item){
    document.getElementById("footer").innerHTML = document.getElementById(item).innerHTML;
}