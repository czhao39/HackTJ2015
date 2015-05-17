var root; var cache; var isDem;
var code_to_state = { "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District Of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming" };
google.load("visualization", "1", {packages:["corechart"]});

function drawChart(clr, sid) {
    var chart = new google.visualization.PieChart($("#pie-overlay")[0])
        chart.draw(google.visualization.arrayToDataTable([['Type', 'Tweets'],['Positive', cache[sid][0]],['Negative', cache[sid][1]]]), {
            title: code_to_state[sid],
            is3D: true,
            //chartArea:{left:0,top:0,width:"100%",height:"100%"},
            backgroundColor: { fill:'transparent' },
            width:200,
            height:200,
            colors: clr,
            legend: { position:'none' }
        });
}
var a = '';
$(document).ready(function() {
    $("#logo").click(function() {
        if (a != '') {
            a = '';
        }
        else {
            a = '_';
        }
    });
    svg = document.getElementById('map');
    svg.addEventListener("load", function() {
        svg = svg.contentDocument;
        root = svg.getElementsByTagName('svg')[0];
        paths = root.getElementsByTagName('path');
       for (i = 0; i < paths.length; i++) {
            var pn = paths[i].id;
            var elm = svg.getElementById(pn);
            if (elm != null) {
                elm.addEventListener("click", function() {
                    var sid = this.id;
                    if (sid == "MI-" || sid == "SP-") {
                        sid = "MI";
                    }
                    $.getJSON("/state?s=" + encodeURIComponent(sid), function(data) {
                        console.log(data);
                    });
                });
                svg.addEventListener("mousemove", function(e) {
                    var rekt = $("#map")[0].getBoundingClientRect();
                    $("#pie-overlay").css({'top':rekt.top+window.scrollY+e.clientY+5,'left':window.scrollX+rekt.left+e.clientX+5});
                });
                elm.addEventListener("mouseover", function(e) {
                    var sid = this.id;
                    if (cache === undefined) {
                        return;
                    }
                    if (sid == "SP-" || sid == "MI-") {
                        sid = "MI";
                    }
                    drawChart([!isDem ? "#FF0000" : "#0000FF", !isDem ? "#0000FF" : "#FF0000"], sid);
                    $("#pie-overlay").show();
                });
                elm.addEventListener("mouseout", function(e) {
                    $("#pie-overlay").hide();
                });
            }
        }
    });

    $(".dem").each(function(index,value) {
        var tmp = $(this);
        $.getJSON("/nation?p=" + encodeURIComponent($(dems).text()), function(data) {
            cache = data;
            tpos = 0
            tneg = 0
            for (var key in data) {
                tpos += data[key][0];
                tneg += data[key][1];
            }
            amt = 1 - (tpos / (tpos + tneg))
            tmp.css("background", "-webkit-linear-gradient(left, #3399cc " + Math.round(amt * 100) + "%,#ffffff 0%)");
        });
    });

    $(".rep").each(function(index, value) {
        var tmp = $(this);
        $.getJSON("/nation?p=" + encodeURIComponent($(reps).text()), function(data) {
            cache = data;
            tpos = 0
            tneg = 0
            for (var key in data) {
                tpos += data[key][0];
                tneg += data[key][1];
            }
            amt = 1 - (tpos / (tpos + tneg))
            tmp.css("background", "-webkit-linear-gradient(left, #cc9933 " + Math.round(amt * 100) + "%,#ffffff 0%");
        })






    })

    var mx = 0;
    var my = 0;
    $(window).mousemove(function(e) {
        mx = e.pageX;
        my = e.pageY;
        $("#img-overlay").css({'top':my+20, 'left':mx+20});
    });
    $("button[data-over]").mouseover(function(e) {
        $("#img-overlay img").attr("src", "/img/pic/" + $(this).attr("data-over") + a + ".jpg");
        var ct = $(this).hasClass("dem");
        $("#img-overlay img").css("border-color", ct ? "#717ECD" : "#CF5C60");
        $("#img-overlay").show();
    }).mouseout(function() {
        $("#img-overlay").hide();
    });
    $("#dem button, #rep button").click(function(e) {
        e.preventDefault();
        $("#state-table-body").empty();
        var ct = $(this).hasClass("dem") ? "rgba(0,0,255," : "rgba(255,0,0,";
        isDem = $(this).hasClass("dem");
        $.getJSON("/nation?p=" + encodeURIComponent($(this).text()), function(data) {
            cache = data;
            for (var key in data) {
                pos = data[key][0];
                neg = data[key][1];
                total = pos + neg;
                ppos = (pos / total * 100).toFixed(2);
                pneg = (neg / total * 100).toFixed(2);
                $("#state-table-body").append("<tr><td>" + code_to_state[key] + "</td><td>" + pos + " tweets</td><td>" + ppos + "%</td><td>" + neg + " tweets</td><td>" + pneg + "%</td></tr>");
                // hardcoded michigan because separation
                var clr = ct;
                if (key == "MI") {
                    key = "MI-";
                    data["MI-"] = clr;
                    svg.getElementById("SP-").style.fill = ct+pos/total+")";
                }
                var elm = svg.getElementById(key);
                elm.style.fill = ct+pos/total+")";
            }
        });
    });
});

