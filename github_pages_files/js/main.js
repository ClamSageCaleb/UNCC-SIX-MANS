$(function () {
  $.ajax({
    type: "get",
    url: "https://uncc-six-mans.s3.amazonaws.com/Leaderboard.json",
    dataType: "json",
    success: (data) => populateTable(data),
  });
  setScrollBar();
  $(window).resize(setScrollBar);
});

function populateTable(ballChasers) {
  not_enough_matches = [];
  ballChasers.forEach((ballChaser, index) => {
    $("#leaderboard-table > tbody").append(
      `<tr>
            <td headers="name">${index + 1}</td>
            <td headers="name">${ballChaser["Name"]}</td>
            <td headers="wins">${ballChaser["Wins"]}</td>
            <td headers="losses">${ballChaser["Losses"]}</td>
            <td headers="matches-played">${ballChaser["Matches Played"]}</td>
            <td headers="win-perc">${parseInt(
              ballChaser["Win Perc"] * 100
            )}%</td>
        </tr>`
    );
  });
}

function setScrollBar() {
  $("#content").css(
    "height",
    window.innerHeight - $("header")[0].getBoundingClientRect().height
  );
}
