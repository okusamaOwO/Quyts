document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    const dislikeButtons = document.querySelectorAll('.dislike-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = event.target.dataset.postId;
            updateLike(postId);
        });
    });

    dislikeButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = event.target.dataset.postId;
            updateDislike(postId);
        });
    });

    function updateLike(postId) {
        fetch(`/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const likeButton = document.querySelector(`.like-btn[data-post-id="${postId}"]`);
            likeButton.innerHTML = `Like (${data.post_like})`;
        });
    }

    function updateDislike(postId) {
        fetch(`/dislike/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const dislikeButton = document.querySelector(`.dislike-btn[data-post-id="${postId}"]`);
            dislikeButton.innerHTML = `Dislike (${data.post_dislike})`;
        });
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
});