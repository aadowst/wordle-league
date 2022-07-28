function compareScoresOriginal() {

    if (document.getElementById("p1d1").value && document.getElementById("p2d1").value) {
        if (document.getElementById("p1d1").value > document.getElementById("p2d1").value) {
            document.getElementById("p1d1").classList.add("green");
            document.getElementById("p2d1").classList.add("grey");
        } else if (document.getElementById("p1d1").value == document.getElementById("p2d1").value) {
            document.getElementById("p1d1").classList.add("yellow");
            document.getElementById("p2d1").classList.add("yellow");
        } else {
            document.getElementById("p1d1").classList.add("grey");
            document.getElementById("p2d1").classList.add("green");
        }
    }
}

function compareScores() {
    let user1Score = 0;
    let user2Score = 0;
    for (let i = 1; i <= 5; i++) {

        if (document.getElementById(`p1d${i}`).value && document.getElementById(`p2d${i}`).value) {

            if (document.getElementById(`p1d${i}`).value < document.getElementById(`p2d${i}`).value) {
                document.getElementById(`p1d${i}`).classList.add("green");
                document.getElementById(`p2d${i}`).classList.add("grey");
                user1Score+=3
            } else if (document.getElementById(`p1d${i}`).value == document.getElementById(`p2d${i}`).value) {
                document.getElementById(`p1d${i}`).classList.add("yellow");
                document.getElementById(`p2d${i}`).classList.add("yellow");
                user1Score++
                user2Score++
            } else {
                document.getElementById(`p1d${i}`).classList.add("grey");
                document.getElementById(`p2d${i}`).classList.add("green");
                user2Score+=3
            }
        }
    }
    document.getElementById('user1-score').innerText = user1Score
    document.getElementById('user2-score').innerText = user2Score

    if(user1Score>user2Score){
        document.getElementById('user1-score').classList.add("green-text")
        document.getElementById('user1-name').classList.add("green-text")
        document.getElementById('user2-score').classList.add("grey-text")
        document.getElementById('user2-name').classList.add("grey-text")
    }
    if(user1Score<user2Score){
        document.getElementById('user1-score').classList.add("grey-text")
        document.getElementById('user1-name').classList.add("grey-text")
        document.getElementById('user2-score').classList.add("green-text")
        document.getElementById('user2-name').classList.add("green-text")
    }

}

function flipCardsHelper(classes) {
    let cards = document.getElementsByClassName(classes)
    for (let i = 0; i < cards.length; i++) {
        cards[i].classList.add("flip")
    }
}
function flipCards(){
    flipCardsHelper('flip-card d000')
    setTimeout(() => {flipCardsHelper('flip-card d100'); }, 250)
    setTimeout(() => {flipCardsHelper('flip-card d200'); }, 500)
    setTimeout(() => {flipCardsHelper('flip-card d300'); }, 750)
    setTimeout(() => {flipCardsHelper('flip-card d400'); }, 1000)

}
