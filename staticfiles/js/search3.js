function searchMonth(tb) {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;

  select1 = 3;
  select2 = 4;
  input1 = "";
  input2 = "";
  if (tb == "table2") {
    input1 = document.getElementById("month");
    input2 = document.getElementById("year");
  } else {
    input1 = document.getElementById("month1");
    input2 = document.getElementById("year1");
  }
  filter1 = input1.value.toUpperCase();
  filter2 = input2.value.toUpperCase();
  table = document.querySelector("." + tb);
  tr = table.querySelectorAll("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[+select1];
    td2 = tr[i].getElementsByTagName("td")[+select2];
    if (td1) {
      txtValue = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;

      if (
        txtValue.toUpperCase().indexOf(filter1) > -1 &&
        txtValue2.toUpperCase().indexOf(filter2) > -1
      ) {
        console.log(txtValue);
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
