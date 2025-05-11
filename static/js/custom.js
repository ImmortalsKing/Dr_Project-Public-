function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_area').scrollIntoView({behavior: 'smooth'})
}

function scrollToAbout() {
    const aboutSection = document.querySelector(".about");
    if (aboutSection) {
        aboutSection.scrollIntoView({behavior: "smooth"});
    }
}

document.getElementById("filter-options").addEventListener("change", function () {
    window.location.href = this.value;
});

document.getElementById('profile_photo').addEventListener('change', function () {
        document.getElementById('avatarForm').submit();
});

function toggleFaqForm() {
    var form = document.getElementById("faq-form");
    form.classList.toggle("open");
}