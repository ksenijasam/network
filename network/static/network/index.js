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


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function saveEditPost (id) {
    try {
        var editedPostContent = document.getElementById('editPostTextarea_' + id).value;

        var postContentElement = document.getElementById('postContent_' + id);
        postContentElement.innerHTML = editedPostContent;

        var editButton = document.getElementById('edit_' + id);
        var cancelButton = document.getElementById('cancelButtonDiv_' + id);
        var savePostButton = document.getElementById('savePostButton_' + id);
        var editPostElement = document.getElementById('editPost_' + id);

        postContentElement.style.display = 'block';
        editButton.style.display = 'block';
        cancelButton.style.display = 'none';
        savePostButton.style.display = 'none';
        editPostElement.style.display = 'none';

        const csrftoken = getCookie('csrftoken');
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        };

        fetch('/saveEditedPost/'+ id, {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify({
              id: id,
              editedPost: editedPostContent
            })
        })
    }
    catch {
        alert('Error occured, please try again.');
    }
}

function liked(id) {
    var emptyHeart = document.getElementById('emptyHeart_' + id);
    var fullHeart = document.getElementById('fullHeart_' + id);

    fullHeart.innerHTML = '<i class="fa-solid fa-heart"></i>';

    emptyHeart.style.display = 'none';
    fullHeart.style.display = 'block';

}