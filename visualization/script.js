
function makeChart(config, caption) {
    var ctx = document.getElementById('myChart').getContext('2d');
    if (chart) {
        chart.destroy();
    }
    document.getElementById("caption").style.display = "block";
    document.getElementById("caption").innerHTML= caption;

    chart = new Chart(ctx, config);
    chart.update(2000);
}

function tog(el) { 
    removeCurrentActive();
    
    var switchEl = document.getElementById("switch");
    switchEl.style.visibility = el.id.includes("level") ? "hidden" : "visible";

    el.classList.add("active");
    makeChart(config_dict[el.id], captions[el.id]);
    console.log(el.id);
}

function toggle_course(el) {
    if (chart) {
        chart.destroy();
    }
    removeCurrentActive();
    document.getElementById("caption").style.display = "none";


    if (el.innerHTML.includes("1x")) {
        setUp(true);
        el.innerHTML = "Switch to 2x data";
    } else {
        setUp(false);
        el.innerHTML = "Switch to 1x data";
    }
}

function removeCurrentActive() {
    var current = document.getElementsByClassName("active");
    if (current.length == 1) {
       current[0].classList.remove("active");
    }
}

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}