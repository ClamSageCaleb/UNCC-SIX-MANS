$(() => loadWinners())

const dataBaseUrl = "https://uncc-six-mans.s3.amazonaws.com/winners";
const winnerFiles = ["summer2020.json", "fall2020.json"];

const loadWinners = async () => {
  for (const file of winnerFiles) {
    const data = await fetch(`${dataBaseUrl}/${file}`).then((res) => res.json())
    data.forEach((player, index) => populateWinners(player, index + 1, file.replace(".json", "")))
  }

  $("#accordion").accordion({
    collapsible: true,
    icons: { header: "accordionClosed", activeHeader: "accordionOpen" },
    heightStyle: "content",
  })
}

function populateWinners(winnerDetails, rank, tableId) {
  $(`#winners-table-${tableId} > tbody`).append(
    `<tr>
      <td headers="rank">${rank}</td>
      <td headers="name">${winnerDetails["Name"]}</td>
      <td headers="wins">${winnerDetails["Wins"]}</td>
      <td headers="losses">${winnerDetails["Losses"]}</td>
      <td headers="matches-played">${winnerDetails["Wins"] + winnerDetails["Losses"]}</td>
      <td headers="win-perc">${Math.round(
        (winnerDetails["Wins"] / (winnerDetails["Wins"] + winnerDetails["Losses"])) * 100
      )}%</td>
    </tr>`
  )
}
