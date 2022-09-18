$(document).ready(function () {
  $("#container-song-battle").show();
  $("#container-song-buildings").hide();
  $("#container-song-route").hide();

  $(".battle-button-trigger").on("click", function () {
    $("#container-song-battle").show();
    $("#container-song-buildings").hide();
    $("#container-song-route").hide();
  });

  $(".buildings-button-trigger").on("click", function () {
    $("#container-song-battle").hide();
    $("#container-song-buildings").show();
    $("#container-song-route").hide();
  });

  $(".route-button-trigger").on("click", function () {
    $("#container-song-battle").hide();
    $("#container-song-buildings").hide();
    $("#container-song-route").show();
  });
});
