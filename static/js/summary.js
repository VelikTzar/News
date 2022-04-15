var element = document.getElementsByClassName("text-body")
var button = document.getElementsByClassName("btn")
var summary = JSON.parse(document.getElementById("summary").textContent)
var content = JSON.parse(document.getElementById("content").textContent)
function Summarize(element, button){
            element.innerHTML = summary
            button.innerHTML =  "Display full text"
        }

function FullText(element, button){

            element.innerHTML = content
            button.innerHTML =  "Display Al-generated summary"
        }
function buttonResponse(){
            if (element.innerHTML === content ){
                Summarize(element, button)
            }
            else if(element.innerHTML === summary){
                FullText(element, button)
            }
        }