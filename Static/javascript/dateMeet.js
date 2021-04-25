// This JS file contains all JS code for the dateMeet app

function generate_html(business){

    return `
            <div class="card my-3" style="width: 18rem;">
                <img src="${business.image_url}" class="card-img-top" alt="yelp_business_img">
                <div class="card-body">
                    <h5 class="card-title">${business.name}</h5>
                    <p class="card-text">${business.location.display_address.toString()}</p>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item"><b>Phone #</b>: ${business.phone_num}</li>
                    <li class="list-group-item"><b>Closed</b>: ${business.is_closed}</li>
                    <li class="list-group-item"><b>Yelp Rating</b>: ${business.rating}</li>
                </ul>
                <div class="card-body">
                    <a href="${business.yelp_url}" class="btn btn-outline-danger btn-lg" role="button" aria-pressed="true">View on Yelp</a>
                </div>
            </div>
    `
}


async function retrieveBusinessInfo(evt){
    // This function is used to make a request to the back end to retrieve business 
    // Information from the yelp api.

    // We want to make sure that the default behavior of a form is prevented 
    evt.preventDefault();

    // Then we retrieve the information entered by the user as interest and send the request to
    // The back end.

    const $userInterest = $('#interest').val();

    resp = await axios.post(`/dateMeet/api/yelp-business-search`,
                            {
                                'interest': $userInterest
                            });

  console.log(resp.data)

  let businesses = resp.data['businesses']

  if (businesses.length < 1){
      console.log('Not much to see here tbh')
      $("#business_display").empty()
      let no_business = $(`<h3>Sorry there are no businesses matching your interest within this location</h3>`)
      $("#business_display").append(no_business)
 
  }
  else{
      $("#business_display").empty()
      for (const business of businesses){

        let new_business = $(generate_html(business))
        $("#business_display").append(new_business)

      }
  }

}

$("#interestform").on("submit", retrieveBusinessInfo)




