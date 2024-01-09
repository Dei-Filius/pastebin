fetch("http://188.166.175.58:31165/letters?id=1")
    .then((res) => {
        res.json();
    })
    .then((data) =>
        fetch("http://188.166.175.58:31165/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: data }),
        }).then()
    );
