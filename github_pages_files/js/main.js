$(function () {
  $.ajax({
    type: "get",
    url: "https://uncc-six-mans.s3.amazonaws.com/Leaderboard.json",
    dataType: "json",
    success: (data) => populateTable(data),
  })
  setScrollBar()
  $(window).resize(setScrollBar)
  $("#lbSearch").keyup((e) => filterLeaderboard(e.target.value))
})

function populateTable(ballChasers, query = null) {
  $("#leaderboard-table > tbody").empty()
  ballChasers.forEach((ballChaser, index) => {
    if (!query || ballChaser["Name"].toLowerCase().includes(query.toLowerCase())) {
      $("#leaderboard-table > tbody").append(
        `<tr>
              <td headers="rank">${index + 1}</td>
              <td headers="name">${ballChaser["Name"]}</td>
              <td headers="wins">${ballChaser["Wins"]}</td>
              <td headers="losses">${ballChaser["Losses"]}</td>
              <td headers="matches-played">${ballChaser["Matches Played"]}</td>
              <td headers="win-perc">${parseInt(ballChaser["Win Perc"] * 100)}%</td>
          </tr>`
      )
    }
  })
  // this prevents page jumping when filtering
  $("#leaderboard").css("min-height", $("#leaderboard").height())
}

function setScrollBar() {
  $("#content").css("height", window.innerHeight - $("header")[0].getBoundingClientRect().height)
}

function filterLeaderboard(query) {
  $("#leaderboard-table > tbody  > tr").each((_, tr) => {
    const playerName = $(tr).children()[1].innerText.toLowerCase()
    if (playerName.includes(query.toLowerCase())) $(tr).show("fade")
    else $(tr).hide("fade")
  })
}
