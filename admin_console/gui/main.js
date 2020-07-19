document.addEventListener('DOMContentLoaded', getAllData);

function getAllData() {
  getQueue();
  getActiveMatches();
  getLeaderboard();
  getConfig();
  document.getElementById("plainText").onchange = handleConfigCheckChange;
}

function getQueue() {
  const queueArea = document.getElementById("queue-select");
  queueArea.innerHTML = "";

  eel.getCurrentQueue()((currQueue) => {
    document.getElementById("queue-timer").innerText = "Time Reset: " + currQueue["timeReset"]

    const queue = currQueue["queue"];

    queue.forEach(player => {
      const content = document.createElement("option");

      content.append(player["name"]);
      content.value = player["name"];
      queueArea.append(content);
    });
  });
}

function getActiveMatches() {
  const activeMatchesArea = document.getElementById("active-matches").getElementsByClassName("matches-content")[0];

  eel.getActiveMatches()((activeMatches) => {
    let content = "";
    activeMatches.forEach((match, index) => {
      content +=
        `<div class="card">
      <div class="card-content">
      <p>Match ${index + 1}</p>
      <hr />
      <div class="col-headers">
        <span>Player</span>
        <span>Team</span>
        <span>Reported</span>
      </div>
      <hr />
      `;
      match["blueTeam"].forEach(bluePlayer => {
        content +=
          `<div class="player">
        <span>${bluePlayer}</span>
        <span>Blue</span>
        <span>${match["reportedWinner"]["player"]["Name"] === bluePlayer}</span>
        </div>`;
      });
      match["orangeTeam"].forEach(orangePlayer => {
        content +=
          `<div class="player">
        <span>${orangePlayer}</span>
        <span>Orange</span>
        <span>${match["reportedWinner"]["player"]["name"] === orangePlayer}</span>
        </div>`;
      })
      content += "</div></div>"
    })
    activeMatchesArea.innerHTML = content;
  })
}

function getLeaderboard() {
  const leaderboardArea = document.getElementById("leaderboard").getElementsByTagName("tbody")[0];
  leaderboardArea.innerHTML = "";
  eel.getLeaderboard()((players) => {
    players.forEach(player => {
      leaderboardArea.innerHTML +=
        `<tr>
        <td headers="name">${player["Name"]}</td>
        <td headers="wins">${player["Wins"]}</td>
        <td headers="losses">${player["Losses"]}</td>
        <td headers="matches-played">${player["Matches Played"]}</td>
        <td headers="win-perc">${parseInt(player["Win Perc"] * 100)}</td>
      </tr>`
    });
  })
}

function getConfig() {
  eel.getConfig()((ret) => {
    document.getElementById("awsId").value = ret["aws_access_key_id"];
    document.getElementById("awsKey").value = ret["aws_secret_access_key"];
    document.getElementById("discordBotKey").value = ret["token"];
  })
}

function handleConfigCheckChange(e) {
  const type = e.target.checked ? "text" : "password"
  document.getElementById("awsId").type = type;
  document.getElementById("awsKey").type = type;
  document.getElementById("discordBotKey").type = type;
}