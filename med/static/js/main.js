$(document).ready(function(){

    $('.button_hide').click(function(){
        $('.block').toggleClass('opener');
        if (!$(this).data('status')) {
            $(this).data('status', true).html('Скрыть текст');
        } else {
            $(this).data('status', false).html('Показать полностью');
        }
    });

});