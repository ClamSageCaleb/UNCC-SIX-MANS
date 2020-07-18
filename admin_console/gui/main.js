document.addEventListener('DOMContentLoaded', getAllData);

function getAllData() {
  getQueue();
  getActiveMatches();
  getLeaderboard();
  getConfig();
}

function getQueue() {
  const queueArea = document.getElementById("queue");
  queueArea.innerHTML = "";

  eel.getCurrentQueue()((currQueue) => {
    Object.keys(currQueue).forEach(key => {
      const content = document.createElement("p");

      let innerContent = currQueue[key];
      if (innerContent === "" || (innerContent instanceof Array && innerContent.length === 0)) {
        innerContent = "None";
      }

      content.append(`${key} - ${innerContent}`);
      queueArea.append(content);
    });
  })
}

function getActiveMatches() {
  const activeMatchesArea = document.getElementById("activeMatches");
  eel.getActiveMatches()((ret) => console.log(ret))
}

function getLeaderboard() {
  const leaderboardArea = document.getElementById("leaderboard");
  eel.getLeaderboard()((ret) => console.log(ret))
}

function getConfig() {
  const configArea = document.getElementById("config");
  eel.getConfig()((ret) => console.log(ret))
}