document.addEventListener("DOMContentLoaded", function () {
  var cdpSwitch = document.getElementById("cdpToggleSwitch");
  var lldpSwitch = document.getElementById("lldpToggleSwitch");

  cdpSwitch.addEventListener("change", function () {
    updateSwitchState("cdp", cdpSwitch.checked);
  });

  lldpSwitch.addEventListener("change", function () {
    updateSwitchState("lldp", lldpSwitch.checked);
  });

  function updateSwitchState(switchType, switchState) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/update-switch-state", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    var data = JSON.stringify({
      switchType: switchType,
      switchState: switchState,
    });

    xhr.send(data);
  }
});
