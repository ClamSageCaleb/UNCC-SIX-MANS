$(() => loadWinners());

const dataBaseUrl = "https://uncc-six-mans.s3.amazonaws.com/winners";
const winnerFiles = ["summer2020.json", "fall2020.json", "spring2021.json", "summer2021.json", "fall2021.json"];

const loadWinners = async () => {
  for (const file of winnerFiles) {
    const data = await fetch(`${dataBaseUrl}/${file}`).then((res) => res.json());
    data.forEach((player, index) => populateWinners(player, index + 1, file.replace(".json", "")));
  }

  $("#accordion").accordion({
    collapsible: true,
    icons: { header: "accordionClosed", activeHeader: "accordionOpen" },
    heightStyle: "content",
  });
};

function populateWinners(winnerDetails, rank, tableId) {
  const mmrRow = "MMR" in winnerDetails ? `<td headers="${tableId}-mmr">${winnerDetails["MMR"]}</td>` : null;

  $(`#winners-table-${tableId} > tbody`).append(
    `<tr>
      <td headers="${tableId}-rank">${rank}</td>
      <td headers="${tableId}-name">${winnerDetails["Name"]}</td>
      ${mmrRow}
      <td headers="${tableId}-wins">${winnerDetails["Wins"]}</td>
      <td headers="${tableId}-losses">${winnerDetails["Losses"]}</td>
      <td headers="${tableId}-matches-played">${winnerDetails["Wins"] + winnerDetails["Losses"]}</td>
      <td headers="${tableId}-win-perc">${Math.round(
      (winnerDetails["Wins"] / (winnerDetails["Wins"] + winnerDetails["Losses"])) * 100
    )}%</td>
    </tr>`
  );
}
