$(function () {
    if (!location.hash) location.hash = "about";

    $.ajax({
        type: "get",
        url: "https://uncc-six-mans.s3.amazonaws.com/Leaderboard.json",
        dataType: "json",
        success: (data) => populateTable(data)
    })

    $("#content").css("height", window.innerHeight - 50);
    setActiveTab();

    $("#content").on('scroll', function (e) {
        $('section').each(function () {
            if ($(this).offset().top < window.pageYOffset
                && $(this).offset().top +
                $(this).height() > window.pageYOffset
            ) {
                var data = $(this).attr('id');
                window.location.hash = data;
            }
        });
    });
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

    $("#content").scroll(function () {
        console.log($(this).scrollTop())
        if ($(this).scrollTop() < 850 && location.hash !== "about") location.hash = "about";
        else if ($(this).scrollTop() < 2000 && location.hash !== "documentation") location.hash = "documentation";
        else if (location.hash !== "leaderboard") location.hash = "leaderboard";
    });
}

$(window).on("hashchange", setActiveTab);

function setActiveTab() {
    const activePage = location.hash;
    const pages = ["#about", "#documentation", "#leaderboard"];

    pages.forEach(page => {
        if (activePage === page)
            $(`a[href="${page}"]`).addClass("active");
        else
            $(`a[href="${page}"]`).removeClass("active");
    })
}