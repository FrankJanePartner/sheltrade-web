// toggle user-menu-mobile display
const profileDropdown = document.querySelector('.profile-dropdown');
const userMenuMobile = document.querySelector('.user-menu-mobile');

profileDropdown.addEventListener('click', () => {
    userMenuMobile.style.display = userMenuMobile.style.display === 'flex' ? 'none' : 'flex';
});