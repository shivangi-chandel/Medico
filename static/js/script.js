// slider

document.addEventListener('DOMContentLoaded', function() {

    var slideImages = document.querySelectorAll('.slide'),
        dirRight = document.getElementById('dir-control-right'),
        dirLeft = document.getElementById('dir-control-left'),
        current = 0;
  
    // Apply styling if JavaScript is active
    function jsActive() {
        for (var i = 0; i < slideImages.length; i++) {
            slideImages[i].classList.add('slider-active');
        }
    }
  
    // Reset all slides (remove the active class)
    function reset() {
        for (var i = 0; i < slideImages.length; i++) {
            slideImages[i].classList.remove('slide-is-active');
        }
    }
  
    // Initialize the slider by showing the first slide
    function startSlide() {
        reset();
        slideImages[0].classList.add('slide-is-active');
        setTimeout(function() {
            for (var i = 0; i < slideImages.length; i++) {
                slideImages[i].classList.add('slide-transition');
            }
        }, 20);
    }
  
    // Navigate to the previous slide
    function slideLeft() {
        reset();
        current = (current - 1 + slideImages.length) % slideImages.length;  // Loop back to the last slide
        slideImages[current].classList.add('slide-is-active');
    }
  
    // Navigate to the next slide
    function slideRight() {
        reset();
        current = (current + 1) % slideImages.length;  // Loop back to the first slide
        slideImages[current].classList.add('slide-is-active');
    }
  
    // Event listener for left arrow click
    dirLeft.addEventListener('click', function() {
        slideLeft();
    });
  
    // Event listener for right arrow click
    dirRight.addEventListener('click', function() {
        slideRight();
    });
  
    // Apply styling and start the slider
    jsActive();
    startSlide();
  
    // Optional: Auto slide every 3 seconds and restart from the first slide when reaching the end
    setInterval(function() {
        slideRight();
        if (current === 0) {
            // Once the last slide has been reached, immediately go back to the first slide
            setTimeout(function() {
                reset();
                slideImages[0].classList.add('slide-is-active');
            }, 500); // Small delay to allow transition to the first slide
        }
    }, 5000);
  
  });
  
  
    document.addEventListener("DOMContentLoaded", function () {
      AOS.init({
         
      });
  });

  
document.addEventListener('DOMContentLoaded', function() {
    const swiper = new Swiper('.mobile-slider', {
        slidesPerView: 2, // Show 2 cards
        slidesPerGroup: 1, // Move 1 card at a time
        spaceBetween: 20,
        loop: true, // Enable continuous loop
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            320: {
                slidesPerView: 2, // 1 card for very small screens
            },
            480: {
                slidesPerView: 2, // 2 cards for larger mobile screens
            }
        }
    });
});
(function () {
    'use strict'
    
    const forms = document.querySelectorAll('.needs-validation')
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            
            form.classList.add('was-validated')
        }, false)
    })
})()
// for map
document.addEventListener("DOMContentLoaded", () => {
    const map = L.map('map').setView([20, 78], 5); // Default India view
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    const locationInput = document.getElementById("location");
    const suggestionsList = document.getElementById("suggestions");

    locationInput.addEventListener("input", async () => {
        const query = locationInput.value.trim();

        if (query.length === 0) {
            suggestionsList.innerHTML = "";
            suggestionsList.style.display = "none";
            return;
        }

        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=5`);
            const results = await response.json();

            suggestionsList.innerHTML = ""; // Clear previous suggestions
            suggestionsList.style.display = results.length > 0 ? "block" : "none";

            results.forEach((place) => {
                const listItem = document.createElement("li");
                listItem.textContent = place.display_name;
                listItem.classList.add("list-group-item");

                listItem.addEventListener("click", () => {
                    locationInput.value = place.display_name;
                    suggestionsList.innerHTML = "";
                    suggestionsList.style.display = "none";
                });

                suggestionsList.appendChild(listItem);
            });
        } catch (error) {
            console.error("Error fetching location suggestions:", error);
            suggestionsList.innerHTML = `<li class="list-group-item text-danger">Error fetching suggestions</li>`;
            suggestionsList.style.display = "block";
        }
    });

    document.getElementById("searchButton").addEventListener("click", async () => {
        const query = locationInput.value.trim();
        if (!query) {
            alert("Please enter a location.");
            return;
        }

        // Fetch location details from Nominatim
        const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=5`);
        const results = await response.json();

        if (results.length === 0) {
            alert("No results found.");
            return;
        }

        // Focus on the first result
        const { lat, lon, display_name } = results[0];
        map.setView([lat, lon], 16); // Zoom to street level

        // Add marker and display details
        L.marker([lat, lon]).addTo(map).bindPopup(display_name).openPopup();

        // Fetch nearby hospitals using Overpass API
        const overpassQuery = `[out:json];node["amenity"="hospital"](around:5000,${lat},${lon});out body;`;
        const overpassResponse = await fetch(`https://overpass-api.de/api/interpreter?data=${encodeURIComponent(overpassQuery)}`);
        const overpassData = await overpassResponse.json();

        overpassData.elements.forEach((hospital) => {
            L.marker([hospital.lat, hospital.lon])
                .addTo(map)
                .bindPopup(hospital.tags.name || "Hospital");
        });
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".position-relative")) {
            suggestionsList.innerHTML = "";
            suggestionsList.style.display = "none";
        }
    });
});
