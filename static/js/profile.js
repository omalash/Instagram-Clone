$(document).ready(function () {
	$('.edit-profile').click(() => {
		$('#edit-form').show();
	});

	$('#save-profile').click(() => {
		$('#edit-form').hide();
	});

	$('.search').click((event) => {
		event.preventDefault();
		$('.search-bar').show();
	});

	$('#search-input').keypress((event) => {
		if (event.which === 13) {
			event.preventDefault();
			$('.search-bar form').submit();
		}
	});

	$('.follow-button').click(function () {
		const profile = $(this).data('other-profile');
		console.log(profile);
		const csrf = $('[name=csrfmiddlewaretoken]').val();
		$.ajax({
			type: 'POST',
			url: `/follow_user/${profile}/`,
			dataType: 'json',
			beforeSend: (xhr) => {
				xhr.setRequestHeader('X-CSRFToken', csrf);
			},
			success: (data) => {
				if (data.success) {
					const followersCount = $('#followers-count');
					const followButton = $('.follow-button');
					followersCount.text('Followers: ' + data.followers_count);
					data.is_following ? followButton.text('Follow') : followButton.text('Unfollow');
				}
			},
			error: (error) => {
				console.error(error);
			},
		});
	});

	$('.like-button').click(function () {
		const postId = $(this).data('post-id');
		const csrf = $('[name=csrfmiddlewaretoken]').val();
		$.ajax({
			type: 'POST',
			url: `/like_post/${postId}/`,
			dataType: 'json',
			beforeSend: (xhr) => {
				xhr.setRequestHeader('X-CSRFToken', csrf);
			},
			success: (data) => {
				if (data.success) {
					const likesCount = $(`#likes-count-${postId}`);
					const likeButton = $(this);
					likesCount.text(data.likes_count);
					data.is_liked ? likeButton.text('Like') : likeButton.text('Unlike');
				}
			},
			error: (error) => {
				console.error(error);
			},
		});
	});
});
