for (ex =0; ex < Object.keys(exper).length ; ex++){
                var collapseBody2 = $('<p class ="elabBody" style="margin-left: '+ 2 +'em; padding:0px;margin-bottom: 0rem; font-size: 1.5vmin;" >');
                collapseBody2.append( "<strong>Title: </strong>" + exper[Object.keys(exper)[ex]]["title"] + "<strong> ID: </strong>" + exper[Object.keys(exper)[ex]]["id"]);
                collapseBody2.append("<strong  > Created at: </strong>" + exper[Object.keys(exper)[ex]]["created_at"] + "<br>");
                collapseBody2.append('<p class="elabBody" style="margin-left: 2em;" >' + (exper[Object.keys(exper)[ex]]["body"] + '</p> <br>');
                collapseBody.append(collapseBody2);
            }
