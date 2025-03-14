const chatButton = document.querySelector('.chatbox__button');
const chatContent = document.querySelector('.chatbox__support');
const icons = {
    isClicked: '<i class="fas fa-envelope" style="font-size: clamp(0.7rem, 3vw, 1.5rem);"></i>',
    isNotClicked: '<i class="fas fa-envelope" style="font-size: clamp(0.7rem, 3vw, 1.5rem);"></i>'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
chatbox.display();
chatbox.toggleIcon(false, chatButton);