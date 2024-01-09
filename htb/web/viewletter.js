fetch("http://localhost/letters?id=3").then((res) => {
    fetch("http://localhost/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: res.text() }),
    }).then((res) => console.log(res));
});
