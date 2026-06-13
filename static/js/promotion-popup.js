(function () {
    var popup = document.getElementById('home-promotion');
    if (!popup) {
        return;
    }

    var storageKey = popup.dataset.storageKey;
    var delay = Number(popup.dataset.delay || 4) * 1000;
    var dismissDays = Number(popup.dataset.dismissDays || 14);
    var closeButtons = popup.querySelectorAll('[data-promotion-close]');
    var closeButton = popup.querySelector('.promotion-popup__close');
    var previousFocus = null;

    function dismissalIsCurrent() {
        try {
            var dismissedAt = Number(localStorage.getItem(storageKey));
            var expiresAfter = dismissDays * 24 * 60 * 60 * 1000;
            return dismissedAt && Date.now() - dismissedAt < expiresAfter;
        } catch (error) {
            return false;
        }
    }

    function rememberDismissal() {
        try {
            localStorage.setItem(storageKey, String(Date.now()));
        } catch (error) {
            // The popup can still close when browser storage is unavailable.
        }
    }

    function openPopup() {
        previousFocus = document.activeElement;
        popup.hidden = false;
        document.body.classList.add('promotion-is-open');
        window.requestAnimationFrame(function () {
            popup.classList.add('is-visible');
            closeButton.focus();
        });
    }

    function closePopup() {
        rememberDismissal();
        popup.classList.remove('is-visible');
        document.body.classList.remove('promotion-is-open');
        window.setTimeout(function () {
            popup.hidden = true;
            if (previousFocus && previousFocus.focus) {
                previousFocus.focus();
            }
        }, 250);
    }

    function keepFocusInDialog(event) {
        if (event.key !== 'Tab' || !popup.classList.contains('is-visible')) {
            return;
        }

        var focusable = popup.querySelectorAll(
            'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        var first = focusable[0];
        var last = focusable[focusable.length - 1];

        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    }

    closeButtons.forEach(function (button) {
        button.addEventListener('click', closePopup);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && popup.classList.contains('is-visible')) {
            closePopup();
        }
        keepFocusInDialog(event);
    });

    if (!dismissalIsCurrent()) {
        window.setTimeout(openPopup, delay);
    }
}());
