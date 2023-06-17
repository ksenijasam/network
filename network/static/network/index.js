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

function editPost(id, content) {
    var postContentElement = document.getElementById('postContent_' + id);
    var editPostElement = document.getElementById('editPost_' + id);
    
    var editButton = document.getElementById('edit_' + id);
    var cancelButton = document.getElementById('cancelButtonDiv_' + id);
    cancelButton.innerHTML = '<button type="button" class="btn btn-sm btn-danger" onclick="cancelEditPost(' + id + ')" id="cancel_' + id + '">Cancel</button>'

    var savePostButton = document.getElementById('savePostButton_' + id);
    savePostButton.innerHTML = '<button type="button" class="btn btn-sm btn-success" onclick="saveEditPost(' + id + ')" id="savePost_' + id + '">Save</button>'


    editButton.style.display = 'none';
    cancelButton.style.display = 'block';
    savePostButton.style.display = 'block';

    postContentElement.style.display = 'none';
    editPostElement.style.display = 'block';
    editPostElement.innerHTML = '<textarea id="editPostTextarea_' + id + '" class="width-100 margin-top-20" rows="5">' + content + '</textarea>';
}

function cancelEditPost(id) {
    var postContentElement = document.getElementById('postContent_' + id);
    var editPostElement = document.getElementById('editPost_' + id);

    var editButton = document.getElementById('edit_' + id);
    var cancelButton = document.getElementById('cancelButtonDiv_' + id);
    var savePostButton = document.getElementById('savePostButton_' + id);

    editButton.style.display = 'block';
    cancelButton.style.display = 'none';
    savePostButton.style.display = 'none';

    postContentElement.style.display = 'block';
    editPostElement.style.display = 'none';
}
