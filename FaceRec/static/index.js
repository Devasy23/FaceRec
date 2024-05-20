$(document).ready(function () {
    $("#captureButton").on("click", function () {
        const EmployeeCode = $("#EmployeeCode").val();
        const Name = $("#Name").val();
        const gender = $("#Gender").val();
        const Department = $("#Department").val();
        $.ajax({
            type: "POST",
            url: "/capture",
            data: {"EmployeeCode":EmployeeCode,"Name": Name ,"gender":gender,"Department":Department},  // Send Title value in the request
            success: function (response) {
                console.log(response)
                updateImage();
                enableImage();
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
});

$(document).ready(function () {
    $("#captureButton1").on("click", function () {
        $.ajax({
            type: "POST",
            url: "/capturing",
            success: function (response) {
                console.log(response)
                updateImage();
                enableImage();
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
});






function updateImage(){
    var img = document.getElementById('Image');
    img.src = 'static/Images/uploads/final.png';
    alert(img.src)
}

function enableImage(){
    var imgElement = document.getElementById('Image');
    imgElement.removeAttribute('hidden');
    var uploadElement = document.getElementById('Upload');
    uploadElement.removeAttribute('hidden');
}
myButton.addEventListener("click", function () {
    myPopup.classList.add("show");
});
closePopup.addEventListener("click", function () {
    myPopup.classList.remove("show");
});

window.addEventListener("click", function (event) {
    if (event.target == myPopup) {
        myPopup.classList.remove("show");
    }
});

//Table.html Js

// function add_employee(){
//     window.location ="flk_blueprint/Add_employee";
// }