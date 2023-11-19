'use strict';

setGenerateTextButtonEventListener();
selectFileUploadEventListener();

function setGenerateTextButtonEventListener() {
    var generateTextButton = document.getElementById("generate-text-button");
    generateTextButton.addEventListener('click', function () {
            let chosenModelId = document.getElementById("available-models").selectedIndex
            let wordGenerateNum = document.getElementById("word-num").value
            let tokenCountPerEntry = document.getElementById("token-count").value
            // change later
            sendGenerateAjaxRequest(chosenModelId, wordGenerateNum, tokenCountPerEntry);

        }, false);
}

function selectFileUploadEventListener() {
    var uploadFileButton = document.getElementById("file-input");
    uploadFileButton.addEventListener('change', function () {
        if (this.files.length > 0) {
            // A file has been selected
            var selectedFile = this.files[0];
            var tokenLength = document.getElementById("token-count").value;
            var selectedFileWebpath = saveFile(selectedFile);


            console.log(selectedFile);
            // Use the selected file in an AJAX request or perform other operations
            sendCreateModelAjaxRequest(selectedFile, tokenLength);
        } else {
            console.log("invalid file");
        }
    });
}

function saveFile(selectedFile) {
    // TODO: Make core save source files (e.g. jobs.txt) to a common folder as  
    // {Original name without extension}_{First 6-10?? digits of file's SHA256 checksum}.{Original file extension}
    //  e.g. hello_world.txt will be saved as hello_world_ads8f7.txt
    // Have both the GUI and the webapp use the same folder for that
    // Models folder will remain the same fttb?

    if (selectedFile) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var fileContent = e.target.result;
        var fileName = file.name;
        
        // Check if the file already exists
        if (!fileExists(fileName)) {
          // Save the file if it doesn't already exist
          var blob = new Blob([fileContent], { type: "text/plain;charset=utf-8" });
          saveAs(blob, fileName);
        } else {
          // File already exists, handle accordingly
          console.log("File already exists");
        }
      };
      reader.readAsText(file);
    }
}

function fileExists()

function sendCreateModelAjaxRequest(selectedFile, tokenLength) {
    $.ajax({
        type: "POST",
        url: "/create_model",
        data: {"file_path" : selectedFile, "token_length" : tokenLength},

        success: function(response) {
            let newOption = document.createElement("option");
            newOption.text = response; 
            newOption.value = response;
            
            document.getElementById("available-models").add(newOption);
            document.getElementById("available-models").value=reponse;

        },
        error: function(error) {
            // Handle any errors that occur during the request
            console.log(error);
        }
    })
}

function sendGenerateAjaxRequest(chosenModelId, wordGenerateNum, tokenCountPerEntry) {
    // console.log(chosenModel, wordGenerateNum, tokenCountPerEntry);
    $.ajax({
        type: "POST",
        url: "/generate_sentence",
        // url: "{{ url_for('generate_sentence') }}",
        // data: {"name" : "Jim"},
        data: {"chosen_model_id" : chosenModelId, "word_generate_num" : wordGenerateNum, "token_count_per_entry" : tokenCountPerEntry},
        
        success: function(response) {
            // Handle the response from the server
            let textArea = document.getElementById('generated-text-area')
            textArea.value = "";

            let index = 0;
            function printSentenceWordByWord() {
                if (index < response.length) {
                    textArea.value += response[index] + " "; // Append the string to the text field with a new line
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
