/**
 * Resize function without multiple trigger
 * 
 * Usage:
 * $(window).smartresize(function(){  
 *     // code here
 * });
*/

$(".preloader").fadeOut();

(function($,sr){
  var debounce = function (func, threshold, execAsap) {
    var timeout;

      return function debounced () {
          var obj = this, args = arguments;
          function delayed () {
              if (!execAsap)
                  func.apply(obj, args); 
              timeout = null; 
          }

          if (timeout)
              clearTimeout(timeout);
          else if (execAsap)
              func.apply(obj, args);

          timeout = setTimeout(delayed, threshold || 100); 
      };
  };

  // smartresize 
  jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

})(jQuery,'smartresize');
/**
* To change this license header, choose License Headers in Project Properties.
* To change this template file, choose Tools | Templates
* and open the template in the editor.
*/

var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
  $BODY = $('body'),
  $MENU_TOGGLE = $('#menu_toggle'),
  $SIDEBAR_MENU = $('#sidebar-menu'),
  $SIDEBAR_FOOTER = $('.sidebar-footer'),
  $LEFT_COL = $('.left_col'),
  $RIGHT_COL = $('.right_col'),
  $NAV_MENU = $('.nav_menu'),
  $FOOTER = $('footer');

// Sidebar
function init_sidebar() {
  // TODO: This is some kind of easy fix, maybe we can improve this
  var setContentHeight = function () {
      // reset height
      $RIGHT_COL.css('min-height', $(window).height());

      var bodyHeight = $BODY.outerHeight(),
          footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
          leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
          contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

      // normalize content
      contentHeight -= $NAV_MENU.height() + footerHeight;

      $RIGHT_COL.css('min-height', contentHeight);
  };

  var openUpMenu = function () {
      $SIDEBAR_MENU.find('li').removeClass('active active-sm');
      $SIDEBAR_MENU.find('li ul').slideUp();
  }

  $SIDEBAR_MENU.find('a').on('click', function (ev) {
      var $li = $(this).parent();

      if ($li.is('.active')) {
          $li.removeClass('active active-sm');
          $('ul:first', $li).slideUp(function () {
              setContentHeight();
          });
      } else {
          // prevent closing menu if we are on child menu
          if (!$li.parent().is('.child_menu')) {
              openUpMenu();
          } else {
              if ($BODY.is('nav-sm')) {
                  if (!$li.parent().is('child_menu')) {
                      openUpMenu();
                  }
              }
          }

          $li.addClass('active');

          $('ul:first', $li).slideDown(function () {
              setContentHeight();
          });
      }
  });

  // toggle small or large menu
  $MENU_TOGGLE.on('click', function () {
      if ($BODY.hasClass('nav-md')) {
          $SIDEBAR_MENU.find('li.active ul').hide();
          $SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
      } else {
          $SIDEBAR_MENU.find('li.active-sm ul').show();
          $SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
      }

      $BODY.toggleClass('nav-md nav-sm');

      setContentHeight();

      $('.dataTable').each(function () { $(this).dataTable().fnDraw(); });
  });

  // check active menu
  $SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

  $SIDEBAR_MENU.find('a').filter(function () {
      return this.href == CURRENT_URL;
  }).parent('li').addClass('current-page').parents('ul').slideDown(function () {
      setContentHeight();
  }).parent().addClass('active');

  // recompute content when resizing
  $(window).smartresize(function () {
      setContentHeight();
  });

  setContentHeight();

  // fixed sidebar
  if ($.fn.mCustomScrollbar) {
      $('.menu_fixed').mCustomScrollbar({
          autoHideScrollbar: true,
          theme: 'minimal',
          mouseWheel: { preventDefault: true }
      });
  }
}
// /Sidebar

// Scroll to top button appear
$(document).on('scroll', function() {
  var scrollDistance = $(this).scrollTop();
  if (scrollDistance > 100) {
    $('.scroll-to-top').fadeIn();
  } else {
    $('.scroll-to-top').fadeOut();
  }
});
// Smooth scrolling using jQuery easing
$(document).on('click', 'a.scroll-to-top', function(e) {
  var $anchor = $(this);
  $('html, body').stop().animate({
    scrollTop: ($($anchor.attr('href')).offset().top)
  }, 1000, 'easeInOutExpo');
  e.preventDefault();
});

// Progressbar
$(document).ready(function () {
    if ($(".progress .progress-bar")[0]) {
        $('.progress .progress-bar').progressbar();
    }
});
// /Progressbar

/* COMPOSE */
function init_compose() {

  if (typeof ($.fn.slideToggle) === 'undefined') { return; }

  $('#compose, .compose-close').click(function () {
      $('.compose').slideToggle();
  });

};

$(document).ready(function () {

  init_sidebar();
  init_compose();

});	