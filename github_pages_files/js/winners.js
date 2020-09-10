$(() => loadWinners())

const winnerFiles = ["summer2020.json", "fall2020.json"];

const loadWinners = async () => {
  for (const file of winnerFiles) {
    const data = await fetch(`/github_pages_files/winners/${file}`).then(res => res.json());
    console.log(data, file)
    await getWinners(data, file.replace(".json", ""));
  };

  console.log("accordion");
  $("#accordion").accordion({
    active: false,
    collapsible: true,
    icons: { header: "accordionClosed", activeHeader: "accordionOpen" },
    heightStyle: "content"
  })
}

async function getWinners(winnerData, tableId) {
  // for (const )
  winnerData.forEach(async (winnerDetails, index) => {
    const data = await fetch(`https://discordapp.com/api/users/${winnerDetails.id}`, {
      method: "GET",
      headers: {
        "Authorization": "Bot [token here]"
      }
    }).then(res => res.json());
    populateWinners(data, winnerData[index], index + 1, tableId);
  });

}

function populateWinners(winnerDiscordUser, winnerDetails, rank, tableId) {
  $(`#winners-table-${tableId} > tbody`).append(
    `<tr>
      <td headers="rank">${rank}</td>
      <td headers="name">${winnerDiscordUser.username}#${winnerDiscordUser.discriminator}</td>
      <td headers="wins">${winnerDetails["Wins"]}</td>
      <td headers="losses">${winnerDetails["Losses"]}</td>
      <td headers="matches-played">${winnerDetails["Wins"] + winnerDetails["Losses"]}</td>
      <td headers="win-perc">${parseInt((winnerDetails["Wins"] / (winnerDetails["Wins"] + winnerDetails["Losses"])) * 100)}%</td>
    </tr>`
  )
}
