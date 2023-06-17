// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelector("#all_posts").addEventListener("click", () => get_all_posts());

//     get_all_posts();
//   });

function get_all_posts() {
    // fetch("/get_all_posts")
    // .then((response) => response.json())
    // .then((response) => {
    //     response.forEach((data) => {
    //        document.querySelector("#all_posts_data").innerHTML += 
    //          `<div style="border: 1px solid #a09b9b"><h1>${data.fields.content}</h1></div>`;
    //     });
    // });
}

function editPost() {
    document.getElementById('postContent').style.display = 'none';

    document.getElementById('editPost').style.display = 'block';
    document.getElementById('editPost').innerHTML = '<textarea id="editPostTextarea" class="width-100 margin-top-20" rows="5"></textarea>';
    
}
