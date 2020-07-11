$(function () {
    $.ajax({
        type: "get",
        url: "https://uncc-six-mans.s3.amazonaws.com/Leaderboard.json",
        dataType: "json",
        success: (data) => populateTable(data)
    });
    setScrollBar();
    $(window).resize(setScrollBar)

});

function populateTable(ballChasers) {
    not_enough_matches = [];
    let rank = 0;
    ballChasers.forEach(ballChaser => {
        if (ballChaser["Matches Played"] < 5) {
            not_enough_matches.push(ballChaser["Name"]);
        } else {
            rank += 1;
            $("#leaderboard-table > tbody").append(
                `<tr>
                    <td headers="name">${rank}</td>
                    <td headers="name">${ballChaser["Name"]}</td>
                    <td headers="wins">${ballChaser["Wins"]}</td>
                    <td headers="losses">${ballChaser["Losses"]}</td>
                    <td headers="matches-played">${ballChaser["Matches Played"]}</td>
                    <td headers="win-perc">${parseInt(ballChaser["Win Perc"] * 100)}</td>
                </tr>`
            )
        }
    });
    $("#leaderboard-table > tfoot").append(
        `<tr>
            <td colspan="6">Players with less than 5 matches played:</td>
        </tr>
        <tr>
            <td colspan="6">${not_enough_matches.join(", ")}</td>
        </tr>`
    )
}

function setScrollBar() {
    $("#content").css("height", window.innerHeight - $("header")[0].getBoundingClientRect().height);
}