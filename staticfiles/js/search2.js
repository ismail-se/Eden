function myFunction(e) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;

  select = 1;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.querySelector("table");
  tr = table.querySelectorAll("tr");
  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[+select];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function searchClass(){
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;

  select = 2;
  input = document.getElementById("class");
  filter = input.value.toUpperCase();
  if (filter != ""){
    table = document.querySelector("table");
    tr = table.querySelectorAll("tr");
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[+select];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}

function searchMonth(){
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
    
  select = 3;
  input = document.getElementById("month");
  filter = input.value.slice(0,3);
  if (filter != ""){
    table = document.querySelector("table");
    tr = table.querySelectorAll("tr");
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length; i++) {
      th = tr[0].getElementsByTagName("th");
      td = tr[i].getElementsByTagName("td");
      for (j = select; j < th.length; j++){
        
        ser = tr[0].getElementsByTagName("th")[j].innerText.slice(0,3)
        if (ser != filter){
          th[j].style.display = "none";
          td[j].style.display = "none"; 
        }
        else{
          th[j].style.display = "";
          td[j].style.display = ""; 
        }
      }
    }
  }
  
}