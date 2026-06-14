(function () {
    var launcher = document.querySelector('[data-tracker-toggle]');
    var tracker = document.getElementById('floating-order-tracker');
    var closeButton = document.querySelector('[data-tracker-close]');

    if (!launcher || !tracker || !closeButton) {
        return;
    }

    function openTracker() {
        tracker.hidden = false;
        launcher.setAttribute('aria-expanded', 'true');
        tracker.querySelector('input').focus();
    }

    function closeTracker() {
        tracker.hidden = true;
        launcher.setAttribute('aria-expanded', 'false');
        launcher.focus();
    }

    launcher.addEventListener('click', function () {
        if (tracker.hidden) {
            openTracker();
        } else {
            closeTracker();
        }
    });
    closeButton.addEventListener('click', closeTracker);
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !tracker.hidden) {
            closeTracker();
        }
    });
}());
