// Get all barbers
fetch('https://praiseabarber.herokuapp.com/api/v1/user/barbers/').then((data)=>{
    // console.log(data);
    return data.json();
}).then((completeData)=>{
    // console.log(completeData);
    let barberHtml="";
    let row1="";
    let row2="";
    let row3="";

    for (let i = 0; i <= 12; i++) {
        barber = completeData[i];
        barberHtml += ` <!-- ltn__product-item -->
        <div class="col-lg-4 col-md-4 col-sm-6 col-6">
            <div class="ltn__product-item ltn__product-item-3 text-center">
                <div>
                    <div class="barber-photo">
                        <span class="barber-img"><img src="${barber.profile_img_url}" alt=""></span>
                        <span style="margin-left: 5px;">${barber.firstname} ${barber.lastname}</span>
                    </div>
                </div>
                <div class="product-img">
                    <a href="#"><img src="{barber.display_img_url}" alt="#"></a>
                    <div class="product-hover-action">
                        <ul>
                            <li>
                                <a href="#" title="Likes"><i class="far fa-heart"> <sup>2</sup></i></a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="barber-info">
                    <div>
                        <h2 class="product-title"><a href="#">Hairstyle</a></h2>
                        <h2 class="product-title"><a href="#">${barber.state}, ${barber.city}</a></h2>
                    </div>
                    <div class="product-price">
                        <a href="#" class="btn btn-success">Contact</a>
                    </div>
                </div>
            </div>
        </div>`

        if (i == 2) {
            row1 = `<div class="container">
            <div class="row justify-content-center">
            ${barberHtml}
            </div>
            </div>`
            barberHtml = '';
        }
        else if (i == 5) {
            row2 = `<div class="container">
            <div class="row justify-content-center">
            ${barberHtml}
            </div>
            </div>`;
            barberHtml = '';
        }
        else if (i == 8) {
            row3 = `<div class="container">
            <div class="row justify-content-center">
            ${barberHtml}
            </div>
            </div>`;
            barberHtml = '';
        }
    }
    // console.log(row2)
    document.getElementById("barber_posts").innerHTML=row1 + row2 + row3;

}).catch((err)=>{
    console.log(err);
})


function getBarbersInState(state) {
    /*Displays all barbers in a state */

    fetch(`https://praiseabarber.herokuapp.com/api/v1/user/barbers/?state=${state}`).then((data)=>{
    // console.log(data);
    return data.json();
    }).then((completeData)=>{
        // console.log(completeData);
        let barberHtml="";
        let row = "";
        let rows = "";

        for (let i = 0; i < completeData.length; i++) {
            barber = completeData[i];
            barberHtml += ` <!-- ltn__product-item -->
            <div class="col-lg-4 col-md-4 col-sm-6 col-6">
                <div class="ltn__product-item ltn__product-item-3 text-center">
                    <div>
                        <div class="barber-photo">
                            <span class="barber-img"><img src="${barber.profile_img_url}" alt=""></span>
                            <span style="margin-left: 5px;">${barber.firstname} ${barber.lastname}</span>
                        </div>
                    </div>
                    <div class="product-img">
                        <a href="#"><img src="{barber.display_img_url}" alt="#"></a>
                        <div class="product-hover-action">
                            <ul>
                                <li>
                                    <a href="#" title="Likes"><i class="far fa-heart"> <sup>2</sup></i></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="barber-info">
                        <div>
                            <h2 class="product-title"><a href="#">Hairstyle</a></h2>
                            <h2 class="product-title"><a href="#">${barber.state}, ${barber.city}</a></h2>
                        </div>
                        <div class="product-price">
                            <a href="#" class="btn btn-success">Contact</a>
                        </div>
                    </div>
                </div>
            </div>`
            // Display the result in rows; with a max of three barbers per row
            if (i > 1 && i % 3 === 0) {
                row = `<div class="container">
                <div class="row justify-content-center">
                ${barberHtml}
                </div>
                </div>`
                rows += row;
                barberHtml = '';
            }
        }
        // console.log(row2)
        document.getElementById("barber_posts").innerHTML=rows;

    }).catch((err)=>{
        console.log(err);
    })
}


function getBarbersInCity() {
    /* Displays all barbers in a city of a state */
    const state = document.getElementById('srch_state').value;
    const city = document.getElementById('srch_city').value;

    fetch(`https://praiseabarber.herokuapp.com/api/v1/user/barbers/?state=${state}&city=${city}`).then((data)=>{
    // console.log(data);
    return data.json();
    }).then((completeData)=>{
        // console.log(completeData);
        let barberHtml="";
        let row = "";
        let rows = "";

        for (let i = 0; i < completeData.length; i++) {
            barber = completeData[i];
            barberHtml += ` <!-- ltn__product-item -->
            <div class="col-lg-4 col-md-4 col-sm-6 col-6">
                <div class="ltn__product-item ltn__product-item-3 text-center">
                    <div>
                        <div class="barber-photo">
                            <span class="barber-img"><img src="${barber.profile_img_url}" alt=""></span>
                            <span style="margin-left: 5px;">${barber.firstname} ${barber.lastname}</span>
                        </div>
                    </div>
                    <div class="product-img">
                        <a href="#"><img src="{barber.display_img_url}" alt="#"></a>
                        <div class="product-hover-action">
                            <ul>
                                <li>
                                    <a href="#" title="Likes"><i class="far fa-heart"> <sup>2</sup></i></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="barber-info">
                        <div>
                            <h2 class="product-title"><a href="#">Hairstyle</a></h2>
                            <h2 class="product-title"><a href="#">${barber.state}, ${barber.city}</a></h2>
                        </div>
                        <div class="product-price">
                            <a href="#" class="btn btn-success">Contact</a>
                        </div>
                    </div>
                </div>
            </div>`
            // Display the result in rows; with a max of three barbers per row
            if (i > 1 && i % 3 === 0) {
                row = `<div class="container">
                <div class="row justify-content-center">
                ${barberHtml}
                </div>
                </div>`
                rows += row;
                barberHtml = '';
            }
        }
        // console.log(row2)
        document.getElementById("barber_posts").innerHTML=rows;

    }).catch((err)=>{
        console.log(err);
    })
}


function getCities() {
    /* Appends a new select element to the div element with id=srch.
    This new select element contains cities that belong to the selected state
    from the select element with id=srch_states.
    */

    // A dictionary with state name as key and an array of cities as value
    var dict = {
        "Lagos": ['Ikeja', 'Island', 'Ikoyi', 'Lekki'],
        "Abuja": ['Gwarinpa', 'Apo', 'Life Camp', 'Lokogoma'],
        "Kaduna": ['Ikara', 'Zaria', 'Lere', 'Chikun'],
        "Rivers": ['Port Harcourt', 'Okrika', 'Eleme', 'Bane']
    }

    let selectedState = document.getElementById('srch_state');

    // When a state is selected, generate cities to select from
    if (selectedState) {
        //display barbers in the state
        getBarbersInState(selectedState.value);

        let state = dict[selectedState.value]
        let html = "";

        state.map((city) => {
            html += `<option value="${city}">${city}</option>`
        });
        outputHtml = `
        <option value="" disabled selected>Select City</option>
        ${html}`

        const srch = document.getElementById("srch")
        
        // Create new select element for cities
        const newSelectItem = document.createElement("select")
        // Add class
        newSelectItem.classList.add("form-control")
        // Add id
        newSelectItem.id = 'srch_city';
        // Insert HTML
        newSelectItem.innerHTML = outputHtml
        // If an option is selected call the getBarbersInCity()
        newSelectItem.onchange = getBarbersInCity

        // Before a new select element is appended, check if one with the
        // same id already exists:
        const check = document.getElementById("srch_city")
        if (check) {
            check.remove();
        }

        //append new select element
        srch.appendChild(newSelectItem)
    }
}