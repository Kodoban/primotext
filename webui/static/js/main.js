'use strict';

setGenerateTextButtonEventListener();
selectFileUploadEventListener();

function setGenerateTextButtonEventListener() {
    var generateTextButton = document.getElementById("generateTextButton");
    generateTextButton.addEventListener('click', function () {
            let chosenModelId = document.getElementById("availableModels").selectedIndex
            let wordGenerateNum = document.getElementById("wordNum").value
            let tokenCountPerEntry = document.getElementById("tokenCount").value
            // change later
            sendGenerateAjaxRequest(chosenModelId, wordGenerateNum, tokenCountPerEntry);

        }, false);
}

function selectFileUploadEventListener(input) {
    var uploadedFile = input.files[0];
    var tokenLength = document.getElementById("tokenCount").value;
    
    var formData = new FormData();
    formData.append('user_source_file', uploadedFile);
    formData.append('token_length', tokenLength);

    $.ajax({
        type: "POST",
        url: "/create_model",
        data: formData,
        processData: false,
        contentType: false,

        dataType: 'json',
        success: function(response) {

            //$('#status').html('File uploaded successfully');

            let newOption = document.createElement("option");
            newOption.text = response.model_name; 
            newOption.value = response.model_unique_value;
            
            document.getElementById("availableModels").add(newOption);
            document.getElementById("availableModels").value=newOption.value;

        },
        error: function(error) {
            // Handle any errors that occur during the request
            console.log(error);
        }
    })


}

function sendCreateModelAjaxRequest(selectedFile, tokenLength) {
    $.ajax({
        type: "POST",
        url: "/create_model",
        data: {"file_path" : selectedFile, "token_length" : tokenLength},

        success: function(response) {
            let newOption = document.createElement("option");
            newOption.text = response; 
            newOption.value = response;
            
            document.getElementById("availableModels").add(newOption);
            document.getElementById("availableModels").value=response;

        },
        error: function(error) {
            // Handle any errors that occur during the request
            console.log(error);
        }
    })
}

function sendGenerateAjaxRequest(chosenModelId, wordGenerateNum, tokenCountPerEntry) {
    $.ajax({
        type: "POST",
        url: "/generate_sentence",
        data: {"chosen_model_id" : chosenModelId, "word_generate_num" : wordGenerateNum, "token_count_per_entry" : tokenCountPerEntry},
        
        success: function(response) {
            // Handle the response from the server
            let textbox = document.getElementById('textboxGeneratedText')
            textbox.value = "";

            let index = 0;
            function printSentenceWordByWord() {
                if (index < response.length) {
                    textbox.value += response[index] + " "; // Append the string to the text field with a new line
                    index++;
                    setTimeout(printSentenceWordByWord, Math.floor(Math.random() * 200) + 50); // Set a delay before printing the next string (adjust the delay as needed)
                }
            }

            printSentenceWordByWord()


            // response.forEach(token => {
            //     setTimeout(() => {
            //         textArea.value += token + " ";
            //     })

            // }, 1000) // make dynamic value
            // TODO: dynamic typing
        },
        error: function(error) {
            // Handle any errors that occur during the request
            console.log(error);
        }
    });
}
