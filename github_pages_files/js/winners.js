$(() => loadWinners())

const dataBaseUrl = "https://raw.githubusercontent.com/ClamSageCaleb/UNCC-SIX-MANS/master/github_pages_files/winners"
const winnerFiles = ["summer2020.json"]

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
      <td headers="win-perc">${parseInt(
        (winnerDetails["Wins"] / (winnerDetails["Wins"] + winnerDetails["Losses"])) * 100
      )}%</td>
    </tr>`
  )
}
