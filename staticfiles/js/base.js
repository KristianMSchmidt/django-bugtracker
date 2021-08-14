console.log("Base JS here!")

/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
    console.log("scroll")
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("topnav").style.top = "0";
    } else {
        document.getElementById("topnav").style.top = "-56px";
    }
    prevScrollpos = currentScrollPos;
}

/*  **************  SideBar ************************ */

// Hide submenus
$('#body-row .collapse').collapse('hide');

// Collapse/Expand icon
$('#collapse-icon').addClass('fa-angle-double-left');

// Collapse click
$('[data-toggle=sidebar-colapse]').click(function() {
    SidebarCollapse();
});

function SidebarCollapse() {
    $('.menu-collapsed').toggleClass('d-none');
    $('.sidebar-submenu').toggleClass('d-none');
    $('.submenu-icon').toggleClass('d-none');
    $('#sidebar-container').toggleClass('sidebar-expanded sidebar-collapsed');

    // Treating d-flex/d-none on separators with title
    var SeparatorTitle = $('.sidebar-separator-title');
    if (SeparatorTitle.hasClass('d-flex')) {
        SeparatorTitle.removeClass('d-flex');
    } else {
        SeparatorTitle.addClass('d-flex');
    }

    // Collapse/Expand icon
    $('#collapse-icon').toggleClass('fa-angle-double-left fa-angle-double-right');
}


function reloadDashboard() {
    e = document.getElementById('body-col')
    if (e.innerHTML.indexOf("Tickets by Status") == -1) {
        // dashboard is currently not shown - so reload it
        return true
    }
    // dashboard is already shown - so don't reload it (it's tricky to get canvas sizes correct on reload)
    return false
}