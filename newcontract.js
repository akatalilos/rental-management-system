$(document).ready(function(){
 
    $("#chargepd").change(function(){
    let rentday = new Date($("#rentday").val());
    let returnday = new Date($("#returnday").val());
    let totaldays = dateDiffInDays(rentday, returnday);
    $("#totalcharge").val(totaldays * $("#chargepd").val() );
    $("#reminder").val($("#totalcharge").val() - $("#payinad").val());
  });
    $("#payinad").change(function(){
      $("#reminder").val($("#totalcharge").val() - $("#payinad").val());
    });
  
    $("#btn1").click(function(){
      var data = new FormData();
      data.append("rentday", $("#rentday").val());
      data.append("returnday", $("#returnday").val());
  
      var url = window.origin + "/avaliable_vehicles";
  
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
          $("option").remove();
          for (let dat of  data){
            var option = $("<option>").val(dat["id"]).text(dat["ak"]+" "+dat["brand"]+" "+dat["model"]+" "+dat["displacement"]);
            $("#vehicles").append(option);
          };
        });
      }).catch(function(error){
        console.log(error);
      });
    })
    });
  
    function dateDiffInDays(a, b) {
    const _MS_PER_DAY = 1000 * 60 * 60 * 24;
    return Math.floor((b- a) / _MS_PER_DAY);
    }
  
  
  