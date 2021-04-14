// This JS file contains all JS code for the dateMeet app
// BASE_URL = "http://127.0.0.1:5000";
// async function geocode(evt){
//     // Use the evt item to prevent the default behaviour of a form which is to refresh the page
//     // On submit.
//     evt.preventDefault();
//     // Collect the address entered from the input fields in the form
//     const $address = $('#address').val()
//     const $name = $('#name').val()

//     resp = await axios.get(BASE_URL, {
//                                         params:{
//                                             name: $name,
//                                             address: $address,
//                                         }
//     })

//     console.log(resp)
// }

// let map;

// function initMap() {
//   map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// }

// $("#user_form").on("submit", geocode);


async function retrieveBusinessInfo(evt){
    // This function is used to make a request to the back end to retrieve business 
    // Information from the yelp api.

    // We want to make sure that the default behavior of a form is prevented 
    evt.preventDefault();

    // Then we retrieve the information entered by the user as interest and send the request to
    // The back end.

    const $userInterest = $('#interest').val()

    resp = await axios.get(`http://127.0.0.1:5000/dateMeet/api/yelp-business-search?interest=${$userInterest}`)

    console.log(resp)
}

$("#interestform").on("submit", retrieveBusinessInfo)
