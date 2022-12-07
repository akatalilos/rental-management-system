$(document).ready(function(){

let days = new Date();
let endday = new Date();
endday.setDate(endday.getDate()+6);


function callendar(cal) {
  console.log(cal)

  const tablehead = document.getElementById("thea");
  const tablebody = document.getElementById("tbod");

  while (tablehead.hasChildNodes()) {
    tablehead.removeChild(tablehead.firstChild);
  }
  while (tablebody.hasChildNodes()) {
    tablebody.removeChild(tablebody.firstChild);
  }
  
  let thead = document.getElementById("thea");
  let tbody = document.getElementById('tbod');

  for (let i = 0; i < cal.length; i++){
    let tbrow = document.createElement("tr");
    tbrow.setAttribute("class", "tbrow");
    let colspan = 2;

    for (let j = 0; j < cal[i].length; j++){
      if (i == 0) {
        if (j > 0){
          let th = document.createElement("th");
          th.setAttribute("class", "mth")
          th.setAttribute("scope", "col")
          th.setAttribute("colspan", "2");
          th.innerHTML = cal[i][j].toString();
          tbrow.appendChild(th);
        }

        else {
          let th = document.createElement("th");
          th.setAttribute("class", "mth")
          th.setAttribute("scope", "col")
          th.innerHTML = cal[i][j].toString();
          tbrow.appendChild(th);
        }
        continue;
      }
      if (j == 0) {
        let th2 = document.createElement("th");
        th2.setAttribute("class", "mth2")
        th2.setAttribute("scope", "row");
        th2.innerHTML = cal[i][j].toString();
        tbrow.appendChild(th2);
        continue;
      }
      let tdata = document.createElement("td");
      if(cal[i][j] == ""){
        tdata.setAttribute("class", "tdata");
        tdata.innerHTML = cal[i][j].toString();
        tbrow.appendChild(tdata)
        continue;
      }
      if (cal[i][j] === cal[i][j-1]){
        tbrow.removeChild(tbrow.lastChild);
        tdata.setAttribute("class", "tdata2");
        tdata.setAttribute("colspan", colspan.toString());
        tdata.innerHTML = cal[i][j].toString();
        tbrow.appendChild(tdata)
        colspan++
      }
      else{
          tdata.setAttribute("class", "tdata2");
          tdata.innerHTML = cal[i][j].toString();
          tbrow.appendChild(tdata);
          colspan = 2;
        }
      }
    if (i == 0){
      thead.appendChild(tbrow);
      continue;
    }
    tbody.appendChild(tbrow);
  }   
}

callendar(callent);

document.getElementById("btnf").addEventListener("click",function(){
  endday.setDate(endday.getDate() + 1);
  days.setDate(days.getDate() +1);
  let startday = days.toISOString();
  let lastday = endday.toISOString();
  console.log(lastday);
  calmove(startday, lastday);
});

document.getElementById("btnb").addEventListener("click", function(){
  days.setDate(days.getDate() - 1);
  endday.setDate(endday.getDate() - 1);
  let startday = days.toISOString();
  let lastday = endday.toISOString();
  calmove(startday, lastday);
});

function calmove(startday, endday){
    var data = new FormData();
    data.append("startday", startday);
    data.append("endday", endday);

    var url = window.origin + "/";

    fetch(url,{
      method: "POST",
      body: data
    })

    .then(function(response)
    {
      if(response.status!=200)
      {
        console.log(response.statusText);
      }
      response.json().then(function(data){
        callendar(data);
      });
    }).catch(function(error){
      console.log(error);
    });
  }

});