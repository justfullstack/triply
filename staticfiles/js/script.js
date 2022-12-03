 
// console.log("SCRIPT JS- LOADED...");



// // variable declaration
// let searchInput = document.querySelector(".search-input");
// const body  = document.querySelector("body");
// const dataList =  document.querySelector("#search__suggestions");


// console.log(searchInput);


// searchInput.addEventListener("keyup",  async (e) =>{
//     let searchVal = e.target.value;


//     console.log(searchVal, searchVal.length);

//     // GET USERS
//     let response = await fetch("/search-users/", {
//         body: JSON.stringify({searchText: searchVal}),
//         method: "POST",
//     })


//     let data = await response.json()



//     // handle empty data
//     if (data.length < 1){
//         return;
//     } else {
//         console.log("Users: ", data);
//         dataList.innerHTML = '';


//         data.forEach((cont) => {
//             let option = ` <option value="${cont.username}"></option>`;
//             dataList.insertAdjacentHTML('beforeend', option);
//         })

        
        
//     }


//     // body.innerHTML = '';

//     // console.log(dataList);

//     // GET GROUPS
//     let group_response = await fetch("/search-groups/", {
//         body: JSON.stringify({searchText: searchVal}),
//         method: "POST",
//     })


//     let group_data = await group_response.json()



//     // handle empty data
//     if (group_data.length < 1){
//         return;

//     } else {
//         console.log("Groups: ", group_data);
//         dataList.innerHTML = '';


//         group_data.forEach((cont) => {
//             let option = ` <option value="${cont.username}"></option>`;
//             dataList.insertAdjacentHTML('beforeend', option);
//         })

        
        
//     }

    
// })