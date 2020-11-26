function myFunction(e) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;

  select = document.querySelector("#by").value;
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
function myFunction2(e) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;

  select = document.querySelector("#by2").value;
  input = document.getElementById("myInput2");
  filter = input.value.toUpperCase();
  table = document.querySelector(".table2");
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
