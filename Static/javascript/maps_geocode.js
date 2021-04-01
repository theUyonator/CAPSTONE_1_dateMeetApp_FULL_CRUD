// This JS contains the server side code to make request to Googles Geocoding API
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json";
async function geocode(evt){
    // Use the evt item to prevent the default behaviour of a form which is to refresh the page
    // On submit.
    evt.preventDefault();
    // Collect the address entered from the input fields in the form
    const $address = $('#address').val()

    resp = await axios.get(BASE_URL, {
                                        params:{
                                            address: $address,
                                            key: geocodeAPIKEY
                                        }
    })

    console.log(resp)
}

$("#user-form").on("submit", geocode);
