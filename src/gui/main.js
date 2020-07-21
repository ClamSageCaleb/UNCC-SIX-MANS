document.addEventListener('DOMContentLoaded', documnetLoad);
document.addEventListener('beforeunload', documentClose)

function documnetLoad() {
  getAllData();
  document.getElementById("plainText").onchange = handleConfigCheckChange;
  document.getElementById("config-form").onsubmit = saveConfigChanges;
  document.getElementById("new-reserve-form").onsubmit = addNewReserve;
  window.setInterval(function () {
    getAllData();
  }, 10000);
}

// TODO does not work
function documentClose(e) {
  console.log("run shutdown")
  e.preventDefault()
  eel.shutdown()
}

function getAllData() {
  getQueue();
  getReserves();
  getActiveMatches();
  getLeaderboard();
  getConfig();
  checkNormStatus();
}

function getQueue() {
  const queueArea = document.getElementById("curr-queue-content");
  queueArea.innerHTML = "";
  let content = "";

  eel.getCurrentQueue()((currQueue) => {
    content = `
      <p>Queue Timer: ${currQueue["timeReset"]}</p>
      <hr />
      <div class="col-headers">
        <span></span>
        <span>Player</span>
        <span>Team</span>
        <span>Captain</span>
      </div>
      <hr />
      `;

    const queue = currQueue["queue"];
    const blueTeam = currQueue["blueTeam"];
    const orangeTeam = currQueue["orangeTeam"];

    queue.forEach(player => {
      content +=
        `<div class="player">
        <input id="player-selection-${player["name"]}" class="player-select" type="checkbox"/>
        <label for="player-selection-${player["name"]}">${player["name"]}</label>
        <select>
          <option value="N/A" selected>N/A</option>
          <option value="Blue">Blue</option>
          <option value="Orange">Orange</option>
        </select>
        <input type="checkbox" disabled/>
        </div>`;
    });

    blueTeam.forEach(player => {
      const isCaptain = player["name"] === currQueue["blueCap"]["name"];

      content +=
        `<div class="player">
        <input id="player-selection-${player["name"]}" class="player-select" type="checkbox"/>
        <label for="player-selection-${player["name"]}">${player["name"]}</label>
        <select>
          <option value="N/A">N/A</option>
          <option value="Blue" selected>Blue</option>
          <option value="Orange">Orange</option>
        </select>
        <input type="checkbox" ${isCaptain ? "checked" : ""}/>
        </div>`;
    });

    orangeTeam.forEach(player => {
      const isCaptain = player["name"] === currQueue["orangeCap"]["name"];

      content +=
        `<div class="player">
        <input id="player-selection-${player["name"]}" class="player-select" type="checkbox"/>
        <label for="player-selection-${player["name"]}">${player["name"]}</label>
        <select>
          <option value="N/A">N/A</option>
          <option value="Blue">Blue</option>
          <option value="Orange" selected>Orange</option>
        </select>
        <input type="checkbox" ${isCaptain ? "checked" : ""}/>
        </div>`;
    });
    queueArea.innerHTML = content;
  });
}

function getReserves() {
  const reservePlayerArea = document.getElementById("reserve-players");
  reservePlayerArea.innerHTML = "";
  let content = "";

  eel.getReserves()(reserves => {
    reserves.forEach(player => {
      content +=
        `<div class="reserve-player">
          <input id="player-selection-${player["name"]}" class="player-select" type="checkbox"/>
          <label for="player-selection-${player["name"]}">${player["name"]}</label>
        </div>`
    });
    reservePlayerArea.innerHTML = content;
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

function saveConfigChanges(e) {
  e.preventDefault();
  const newConfig = {
    "aws_access_key_id": document.getElementById("awsId").value,
    "aws_secret_access_key": document.getElementById("awsKey").value,
    "token": document.getElementById("discordBotKey").value,
  }
  eel.setConfig(newConfig)(ret => console.log(ret));
}

function removePlayersFromQueue() {
  const queuedPlayers = Array.from(document.getElementById("curr-queue-content").getElementsByClassName("player-select"));

  eel.getCurrentQueue()((currQueue) => {
    let removedPlayers = [];
    let newQueue = { ...currQueue };
    const queueLists = ["queue", "blueTeam", "orangeTeam"];

    queuedPlayers.forEach((player) => {
      if (player.checked) {
        const playerName = player.id.split("-")[2];

        queueLists.forEach(key => {
          const queueIndex = newQueue[key].findIndex(p => p["name"] === playerName);
          if (queueIndex !== -1) {
            removedPlayers.push(newQueue[key].splice(queueIndex, 1)[0]);
          }
        });
      }
    });

    eel.setCurrentQueue(newQueue)(ret => console.log(ret));

    eel.getReserves()(reserves => {
      let newReserves = Array.from(reserves);
      removedPlayers.forEach(player => newReserves.push(player));

      eel.setReserves(newReserves)(ret => {
        console.log(ret);
        getQueue();
        getReserves();
      });
    });
  })
}

function clearCurrentQueue() {
  eel.getCurrentQueue()((currQueue) => {
    let removedPlayers = [];
    const newQueue = {
      "timeReset": 0,
      "queue": [],
      "orangeCap": "",
      "blueCap": "",
      "orangeTeam": [],
      "blueTeam": []
    };

    eel.getReserves()(reserves => {
      let newReserves = Array.from(reserves);

      const queueLists = ["queue", "blueTeam", "orangeTeam"];
      queueLists.forEach(key => {
        currQueue[key].forEach(player => {
          newReserves.push(player);
        });
      });

      eel.setCurrentQueue(newQueue)(ret => console.log(ret));

      eel.setReserves(newReserves)(ret => {
        console.log(ret);
        getQueue();
        getReserves();
      });
    });
  })
}


function addReservesToQueue() {
  const reservedPlayers = Array.from(document.getElementById("reserve-players").getElementsByClassName("player-select"));
  let playersToAdd = [];

  eel.getReserves()(reserves => {
    const newReserves = Array.from(reserves);

    reservedPlayers.forEach((player) => {
      if (player.checked) {
        const playerName = player.id.split("-")[2];
        const foundIndex = newReserves.findIndex(p => p["name"] === playerName);
        playersToAdd.push(newReserves.splice(foundIndex, 1)[0]);
      }
    });

    eel.setReserves(newReserves)(ret => console.log(ret));

    eel.getCurrentQueue()(currQueue => {
      let newQueue = { ...currQueue };
      playersToAdd.forEach(player => {
        newQueue["queue"].push(player);
      });

      eel.setCurrentQueue(newQueue)(ret => {
        console.log(ret);
        getQueue();
        getReserves();
      });

    });

  });
}

function closeNewReserveModal() {
  const modal = document.getElementById("addReserveModal");
  modal.style.display = "none";
}

function showNewReserveModal() {
  const modal = document.getElementById("addReserveModal");
  modal.style.display = "block";
}

function addNewReserve(e) {
  e.preventDefault();
  const newPlayerId = document.getElementById("playerId").value;
  const newPlayerName = document.getElementById("playerName").value;
  console.log(newPlayerId, newPlayerName);

  eel.getReserves()(reserves => {
    const newReserves = Array.from(reserves);

    newReserves.push({
      "name": newPlayerName,
      "id": newPlayerId,
    });

    eel.setReserves(newReserves)(ret => {
      console.log(ret);
      getReserves();
      closeNewReserveModal();
    });
  });
}

function shutdownNorm() {
  eel.putNormToSleep()(() => {
    checkNormStatus();
  });
}

function startNorm() {
  eel.startNorm()(() => {
    checkNormStatus();
  });
}

function checkNormStatus() {
  const normStatusArea = document.getElementById("normStatus");
  eel.checkNormStatus()((status) => {
    normStatusArea.innerHTML =
      `Norm is 
      <span style="color: ${status ? "green" : "red"}; font-weight: bold;">
        ${status ? "running" : "down"}
      </span>
      <button class="normBtn ${status ? "normOn" : "normOff"}" onclick=${status ? "shutdownNorm()" : "startNorm()"}>${status ? "Shutdown Norm" : "Start Norm"}</button>`;
  });
}