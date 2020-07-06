$(function() {
    $.ajax({
        type: "get",
        url: "https://uncc-six-mans.s3.amazonaws.com/Leaderboard.json",
        dataType: "json",
        success: (data) => populateTable(data)
    })
});

function populateTable(ballChasers) {
    not_enough_matches = [];
    ballChasers.forEach(ballChaser => {
        if (ballChaser["Matches Played"] < 5) {
            not_enough_matches.push(ballChaser["Name"]);
        } else {
            $("#leaderboard-table > tbody").append(
                `<tr>
                    <td headers="name">${ballChaser["Name"]}</td>
                    <td headers="wins">${ballChaser["Wins"]}</td>
                    <td headers="losses">${ballChaser["Losses"]}</td>
                    <td headers="matches-played">${ballChaser["Matches Played"]}</td>
                    <td headers="win-perc">${ballChaser["Win Perc"]}</td>
                </tr>`
            )
        }
    });
    $("#leaderboard-table > tfoot").append(
        `<tr>
            <td colspan="4">Players with less than 5 matches played: ${not_enough_matches.join(",")}</td>
        </tr>`
    )
}