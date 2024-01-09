fetch("http://localhost/message/3")
    .then((res) => res.text())
    .then((data) =>
        fetch("http://localhost/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: data,
        })
    );
