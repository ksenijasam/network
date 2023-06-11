document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#all_posts").addEventListener("click", () => get_all_posts());

    get_all_posts();
  });

function get_all_posts() {
    fetch("/get_all_posts")
    .then((response) => response.json())
    .then((response) => {
        response.forEach((data) => {
           document.querySelector("#all_posts_data").innerHTML += `<div><h1>${data.fields.content}</h1></div>`;
        });
    });
}
