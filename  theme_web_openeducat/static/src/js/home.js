$('.counter-number').each(function () {
    $(this).prop('Counter',0).animate({
        Counter: $(this).text()
    }, {
        duration: 3000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});


// ---------------------------

$('#hamburger').click(function() {
    console.log("click..............");
    $('#hamburger').toggleClass('show');
    $('#overlay').toggleClass('show');
    $('.nav1').toggleClass('show');

  });



// ---------------------------

let imgs=document.querySelectorAll('.change-img');
let imgsrc=document.querySelector('.set-img');
let atds=document.querySelectorAll('.atd');

    function changeImg(imgs) {
        imgs.forEach(img => {
            img.addEventListener('click', () => {

              let imgname=img.querySelector('img').getAttribute('name')


              imgs.forEach(el => el.classList.remove('img-overlay'))
                img.classList.add('img-overlay')
            
                document.querySelectorAll(`.atd`).forEach(el => el.classList.add('d-none'))
                document.querySelector(`.atd[name="${imgname}"]`).classList.remove('d-none')
                
                imgsrc.setAttribute('src',img.querySelector('img').getAttribute('src'))
 
        });
     })
    }


    changeImg(imgs);

// ---------------------------




   