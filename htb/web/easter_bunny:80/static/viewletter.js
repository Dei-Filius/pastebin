fetch("http://localhost/letters?id=3")
    .then((res) => {
        res.json();
    })
    .then((data) =>
        fetch("http://localhost/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: data }),
        }).then()
    );
