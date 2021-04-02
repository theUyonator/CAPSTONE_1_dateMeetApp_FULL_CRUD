// This JS contains the server side code to make request to Googles Geocoding API
BASE_URL = "http://127.0.0.1:5000";
async function geocode(evt){
    // Use the evt item to prevent the default behaviour of a form which is to refresh the page
    // On submit.
    evt.preventDefault();
    // Collect the address entered from the input fields in the form
    const $address = $('#address').val()
    const $name = $('#name').val()

    resp = await axios.get(BASE_URL, {
                                        params:{
                                            name: $name,
                                            address: $address,
                                        }
    })

    console.log(resp)
}

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

$("#user_form").on("submit", geocode);
