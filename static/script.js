const input = document.getElementById("movie");

input.addEventListener("input", async function () {

    const response = await fetch(`/suggest?q=${this.value}`);

    const suggestions = await response.json();

    console.log(suggestions);

});